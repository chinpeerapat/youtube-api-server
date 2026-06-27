from fastapi import APIRouter, Depends

from app.models.youtube import YouTubeRequest
from app.middleware.auth import get_current_user
from app.utils.youtube_tools import YouTubeTools

router = APIRouter(
    prefix="/youtube",
    tags=["youtube"],
    responses={404: {"description": "Not found"}},
)

root_router = APIRouter(
    tags=["youtube"],
    responses={404: {"description": "Not found"}},
)

@router.post("/video-data")
async def get_video_data(
    request: YouTubeRequest,
    _user: dict = Depends(get_current_user),
):
    """Endpoint to get video metadata"""
    return await YouTubeTools.get_video_data(request.url)

@router.post("/video-captions")
async def get_video_captions(
    request: YouTubeRequest,
    _user: dict = Depends(get_current_user),
):
    """Endpoint to get video captions"""
    return await YouTubeTools.get_video_captions(request.url, request.languages)

@router.post("/video-timestamps")
async def get_video_timestamps(
    request: YouTubeRequest,
    _user: dict = Depends(get_current_user),
):
    """Endpoint to get video timestamps"""
    return await YouTubeTools.get_video_timestamps(request.url, request.languages)

@router.post("/video-transcript-languages")
async def get_video_transcript_languages(
    request: YouTubeRequest,
    _user: dict = Depends(get_current_user),
):
    """Endpoint to list available transcript languages"""
    return await YouTubeTools.get_video_transcript_languages(request.url)

@root_router.post("/video-data")
async def get_root_video_data(
    request: YouTubeRequest,
    _user: dict = Depends(get_current_user),
):
    """Reference-compatible endpoint to get video metadata"""
    return await YouTubeTools.get_video_data(request.url)

@root_router.post("/video-captions")
async def get_root_video_captions(
    request: YouTubeRequest,
    _user: dict = Depends(get_current_user),
):
    """Reference-compatible endpoint to get video captions"""
    captions = await YouTubeTools.get_video_captions(request.url, request.languages)
    return {"captions": captions}

@root_router.post("/video-timestamps")
async def get_root_video_timestamps(
    request: YouTubeRequest,
    _user: dict = Depends(get_current_user),
):
    """Reference-compatible endpoint to get video timestamps"""
    timestamps = await YouTubeTools.get_video_timestamps(request.url, request.languages)
    return {"timestamps": timestamps}

@root_router.post("/video-transcript-languages")
async def get_root_video_transcript_languages(
    request: YouTubeRequest,
    _user: dict = Depends(get_current_user),
):
    """Reference-compatible endpoint to list available transcript languages"""
    languages = await YouTubeTools.get_video_transcript_languages(request.url)
    return {"available_languages": languages}
