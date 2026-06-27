from types import SimpleNamespace

import pytest

from app.utils.youtube_tools import YouTubeTools


class FakeSnippet:
    def __init__(self, text: str, start: float) -> None:
        self.text = text
        self.start = start


class FakeTranscript:
    def __init__(self, language_code: str, language: str = "English", is_generated: bool = False) -> None:
        self.language_code = language_code
        self.language = language
        self.is_generated = is_generated
        self.is_translatable = True


def test_get_youtube_video_id_supports_common_url_shapes():
    assert YouTubeTools.get_youtube_video_id("https://www.youtube.com/watch?v=abc123") == "abc123"
    assert YouTubeTools.get_youtube_video_id("https://youtu.be/abc123") == "abc123"
    assert YouTubeTools.get_youtube_video_id("https://youtube.com/embed/abc123") == "abc123"
    assert YouTubeTools.get_youtube_video_id("https://www.youtube.com/v/abc123") == "abc123"
    assert YouTubeTools.get_youtube_video_id("https://example.com/watch?v=abc123") is None


def test_select_languages_prefers_requested_available_language():
    transcripts = [FakeTranscript("en"), FakeTranscript("hi", "Hindi")]

    assert YouTubeTools._select_languages(transcripts, ["es", "hi"]) == ["hi"]


def test_select_languages_falls_back_to_english_then_first_available():
    assert YouTubeTools._select_languages([FakeTranscript("en"), FakeTranscript("hi")], None) == ["en"]
    assert YouTubeTools._select_languages([FakeTranscript("th", "Thai")], ["es"]) == ["th"]


@pytest.mark.asyncio
async def test_get_video_captions_uses_fallback_transcript(monkeypatch):
    async def fake_to_thread(func, *args):
        return (
            [FakeSnippet("hello", 0), FakeSnippet("world", 1)],
            [FakeTranscript("en")],
        )

    monkeypatch.setattr("app.utils.youtube_tools.asyncio.to_thread", fake_to_thread)

    captions = await YouTubeTools.get_video_captions(
        "https://www.youtube.com/watch?v=abc123",
        ["en"],
    )

    assert captions == "hello world"


@pytest.mark.asyncio
async def test_get_video_timestamps_formats_snippets(monkeypatch):
    async def fake_to_thread(func, *args):
        return (
            [FakeSnippet("intro", 0), FakeSnippet("middle", 65)],
            [FakeTranscript("en")],
        )

    monkeypatch.setattr("app.utils.youtube_tools.asyncio.to_thread", fake_to_thread)

    timestamps = await YouTubeTools.get_video_timestamps("https://youtu.be/abc123")

    assert timestamps == ["0:00 - intro", "1:05 - middle"]


@pytest.mark.asyncio
async def test_get_video_transcript_languages_maps_transcript_metadata(monkeypatch):
    async def fake_to_thread(func, *args):
        return [FakeTranscript("en"), FakeTranscript("hi", "Hindi", True)]

    monkeypatch.setattr("app.utils.youtube_tools.asyncio.to_thread", fake_to_thread)

    languages = await YouTubeTools.get_video_transcript_languages("https://youtu.be/abc123")

    assert languages == [
        {
            "language": "English",
            "language_code": "en",
            "is_generated": False,
            "is_translatable": True,
        },
        {
            "language": "Hindi",
            "language_code": "hi",
            "is_generated": True,
            "is_translatable": True,
        },
    ]


def test_runtime_status_reflects_settings(monkeypatch):
    monkeypatch.setattr("app.utils.youtube_tools.settings.ENABLE_AUTH", True)
    monkeypatch.setattr("app.utils.youtube_tools.settings.AUTH_TYPE", "api_key")
    monkeypatch.setattr("app.utils.youtube_tools.settings.ENABLE_PROXY", True)
    monkeypatch.setattr("app.utils.youtube_tools.settings.PROXY_HOST", "proxy.example")
    monkeypatch.setattr("app.utils.youtube_tools.settings.PROXY_PORT", 8080)
    monkeypatch.setattr("app.utils.youtube_tools.settings.WEBSHARE_PROXY_USERNAME", "user")
    monkeypatch.setattr("app.utils.youtube_tools.settings.WEBSHARE_PROXY_PASSWORD", "pass")
    monkeypatch.setattr("app.utils.youtube_tools.settings.WEBSHARE_PROXY_LOCATIONS", ["us"])

    status = YouTubeTools.get_runtime_status()

    assert status["generic_proxy_enabled"] is True
    assert status["webshare_proxy_enabled"] is True
    assert status["auth_enabled"] is True
    assert status["auth_type"] == "api_key"
