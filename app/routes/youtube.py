from fastapi import APIRouter

from app.models.youtube import YouTubeRequest
from app.utils.youtube_tools import YouTubeTools

router = APIRouter(
    prefix="/youtube",
    tags=["youtube"],
    responses={404: {"description": "Not found"}},
)

@router.post("/video-data")
async def get_video_data(request: YouTubeRequest):
    """Endpoint to get video metadata"""
    return YouTubeTools.get_video_data(request.url)

@router.post("/video-captions")
async def get_video_captions(request: YouTubeRequest):
    """Endpoint to get video captions"""
    return YouTubeTools.get_video_captions(request.url, request.languages)

@router.post("/video-timestamps")
async def get_video_timestamps(request: YouTubeRequest):
    """Endpoint to get video timestamps"""
    return YouTubeTools.get_video_timestamps(request.url, request.languages)
