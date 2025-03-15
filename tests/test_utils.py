"""
Tests for utility functions
"""
import pytest
from app.utils.youtube_tools import YouTubeTools

# Test video URLs and their expected IDs
VIDEO_URLS = [
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ("https://www.youtube.com/v/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ("https://invalid-url.com", None),
]

@pytest.mark.parametrize("url,expected_id", VIDEO_URLS)
def test_get_youtube_video_id(url, expected_id):
    """Test the function to extract video IDs from YouTube URLs"""
    video_id = YouTubeTools.get_youtube_video_id(url)
    assert video_id == expected_id
