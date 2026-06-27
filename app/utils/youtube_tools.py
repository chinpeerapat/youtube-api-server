import json
import asyncio
from urllib.parse import urlparse, parse_qs, urlencode
from typing import Optional, List

from fastapi import HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

from app.core.config import settings
from app.middleware.proxy import proxy_client

class YouTubeTools:
    @staticmethod
    def get_youtube_video_id(url: str) -> Optional[str]:
        """Function to get the video ID from a YouTube URL."""
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        if hostname == "youtu.be":
            return parsed_url.path[1:]
        if hostname in ("www.youtube.com", "youtube.com"):
            if parsed_url.path == "/watch":
                query_params = parse_qs(parsed_url.query)
                return query_params.get("v", [None])[0]
            if parsed_url.path.startswith("/embed/"):
                return parsed_url.path.split("/")[2]
            if parsed_url.path.startswith("/v/"):
                return parsed_url.path.split("/")[2]
        return None

    @staticmethod
    async def get_video_data(url: str) -> dict:
        """Function to get video data from a YouTube URL."""
        if not url:
            raise HTTPException(status_code=400, detail="No URL provided")

        try:
            video_id = YouTubeTools.get_youtube_video_id(url)
            if not video_id:
                raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=400, detail="Error getting video ID from URL") from exc

        try:
            params = {"format": "json", "url": f"https://www.youtube.com/watch?v={video_id}"}
            oembed_url = "https://www.youtube.com/oembed"
            query_string = urlencode(params)
            full_url = oembed_url + "?" + query_string

            response = await proxy_client.get(full_url)
            response.raise_for_status()
            video_data = json.loads(response.text)
            clean_data = {
                "title": video_data.get("title"),
                "author_name": video_data.get("author_name"),
                "author_url": video_data.get("author_url"),
                "type": video_data.get("type"),
                "height": video_data.get("height"),
                "width": video_data.get("width"),
                "version": video_data.get("version"),
                "provider_name": video_data.get("provider_name"),
                "provider_url": video_data.get("provider_url"),
                "thumbnail_url": video_data.get("thumbnail_url"),
            }
            return clean_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting video data: {str(e)}") from e

    @staticmethod
    def _get_video_id_or_raise(url: str) -> str:
        if not url:
            raise HTTPException(status_code=400, detail="No URL provided")

        try:
            video_id = YouTubeTools.get_youtube_video_id(url)
            if not video_id:
                raise HTTPException(status_code=400, detail="Invalid YouTube URL")
            return video_id
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=400, detail="Error getting video ID from URL") from exc

    @staticmethod
    def _create_youtube_api() -> YouTubeTranscriptApi:
        if settings.webshare_proxy_enabled:
            proxy_config = WebshareProxyConfig(
                proxy_username=settings.WEBSHARE_PROXY_USERNAME,
                proxy_password=settings.WEBSHARE_PROXY_PASSWORD,
                filter_ip_locations=settings.WEBSHARE_PROXY_LOCATIONS or None,
            )
            return YouTubeTranscriptApi(proxy_config=proxy_config)

        return YouTubeTranscriptApi()

    @staticmethod
    def _list_transcripts_sync(video_id: str) -> list:
        transcript_list = YouTubeTools._create_youtube_api().list(video_id)
        return list(transcript_list)

    @staticmethod
    def _select_languages(available_transcripts: list, languages: Optional[List[str]]) -> list[str]:
        available_codes = [transcript.language_code for transcript in available_transcripts]
        requested = languages or []

        selected = [language for language in requested if language in available_codes]
        if selected:
            return selected

        if "en" in available_codes:
            return ["en"]

        if available_codes:
            return [available_codes[0]]

        return requested or ["en"]

    @staticmethod
    def _get_transcript_with_fallback_sync(video_id: str, languages: Optional[List[str]] = None):
        available_transcripts = YouTubeTools._list_transcripts_sync(video_id)
        selected_languages = YouTubeTools._select_languages(available_transcripts, languages)
        fetched_transcript = YouTubeTools._create_youtube_api().fetch(
            video_id,
            languages=selected_languages,
        )
        return fetched_transcript, available_transcripts

    @staticmethod
    async def get_video_captions(url: str, languages: Optional[List[str]] = None) -> str:
        """Get captions from a YouTube video."""
        video_id = YouTubeTools._get_video_id_or_raise(url)

        try:
            fetched_transcript, _ = await asyncio.to_thread(
                YouTubeTools._get_transcript_with_fallback_sync,
                video_id,
                languages,
            )

            if fetched_transcript:
                return " ".join(snippet.text for snippet in fetched_transcript)
            return "No captions found for video"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting captions for video: {str(e)}") from e

    @staticmethod
    async def get_video_timestamps(url: str, languages: Optional[List[str]] = None) -> List[str]:
        """Generate timestamps for a YouTube video based on captions."""
        video_id = YouTubeTools._get_video_id_or_raise(url)

        try:
            fetched_transcript, _ = await asyncio.to_thread(
                YouTubeTools._get_transcript_with_fallback_sync,
                video_id,
                languages,
            )

            timestamps = []
            for snippet in fetched_transcript:
                start = int(snippet.start)
                minutes, seconds = divmod(start, 60)
                timestamps.append(f"{minutes}:{seconds:02d} - {snippet.text}")
            return timestamps
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating timestamps: {str(e)}") from e

    @staticmethod
    async def get_video_transcript_languages(url: str) -> List[dict]:
        """List available transcript languages for a video."""
        video_id = YouTubeTools._get_video_id_or_raise(url)

        try:
            available_transcripts = await asyncio.to_thread(
                YouTubeTools._list_transcripts_sync,
                video_id,
            )
            return [
                {
                    "language": transcript.language,
                    "language_code": transcript.language_code,
                    "is_generated": transcript.is_generated,
                    "is_translatable": transcript.is_translatable,
                }
                for transcript in available_transcripts
            ]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error listing transcript languages: {str(e)}",
            ) from e

    @staticmethod
    def get_runtime_status() -> dict:
        """Expose runtime capability status for health checks."""
        return {
            "generic_proxy_enabled": bool(settings.proxy_url),
            "webshare_proxy_enabled": settings.webshare_proxy_enabled,
            "webshare_proxy_locations": settings.WEBSHARE_PROXY_LOCATIONS,
            "auth_enabled": settings.ENABLE_AUTH,
            "auth_type": settings.AUTH_TYPE if settings.ENABLE_AUTH else "disabled",
            "parallel_processing": "enabled",
        }
