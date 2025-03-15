from typing import Optional, List
from pydantic import BaseModel

class YouTubeRequest(BaseModel):
    """
    Model for YouTube API requests.
    
    Attributes:
        url: YouTube video URL
        languages: Optional list of language codes for captions
    """
    url: str
    languages: Optional[List[str]] = None

class VideoData(BaseModel):
    """
    Model for YouTube video metadata.
    
    Attributes:
        title: Video title
        author_name: Channel name
        author_url: Channel URL
        type: Media type
        height: Video height
        width: Video width
        version: API version
        provider_name: Service provider name
        provider_url: Service provider URL
        thumbnail_url: Thumbnail URL
    """
    title: Optional[str] = None
    author_name: Optional[str] = None
    author_url: Optional[str] = None
    type: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None
    version: Optional[str] = None
    provider_name: Optional[str] = None
    provider_url: Optional[str] = None
    thumbnail_url: Optional[str] = None