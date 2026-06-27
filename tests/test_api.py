from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_includes_runtime_fields():
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert "timestamp" in body
    assert "generic_proxy_enabled" in body
    assert "webshare_proxy_enabled" in body
    assert body["parallel_processing"] == "enabled"


def test_video_routes_are_registered():
    paths = {route.path for route in app.routes}

    assert "/youtube/video-data" in paths
    assert "/youtube/video-captions" in paths
    assert "/youtube/video-timestamps" in paths
    assert "/youtube/video-transcript-languages" in paths
    assert "/video-data" in paths
    assert "/video-captions" in paths
    assert "/video-timestamps" in paths
    assert "/video-transcript-languages" in paths


def test_root_caption_endpoint_returns_reference_envelope(monkeypatch):
    async def fake_get_video_captions(url, languages=None):
        assert url == "https://youtu.be/abc123"
        assert languages == ["en"]
        return "caption text"

    monkeypatch.setattr(
        "app.routes.youtube.YouTubeTools.get_video_captions",
        fake_get_video_captions,
    )

    response = client.post(
        "/video-captions",
        json={"url": "https://youtu.be/abc123", "languages": ["en"]},
    )

    assert response.status_code == 200
    assert response.json() == {"captions": "caption text"}


def test_legacy_caption_endpoint_preserves_raw_response(monkeypatch):
    async def fake_get_video_captions(url, languages=None):
        return "caption text"

    monkeypatch.setattr(
        "app.routes.youtube.YouTubeTools.get_video_captions",
        fake_get_video_captions,
    )

    response = client.post("/youtube/video-captions", json={"url": "https://youtu.be/abc123"})

    assert response.status_code == 200
    assert response.json() == "caption text"


def test_root_languages_endpoint_returns_reference_envelope(monkeypatch):
    async def fake_get_video_transcript_languages(url):
        return [{"language_code": "en"}]

    monkeypatch.setattr(
        "app.routes.youtube.YouTubeTools.get_video_transcript_languages",
        fake_get_video_transcript_languages,
    )

    response = client.post("/video-transcript-languages", json={"url": "https://youtu.be/abc123"})

    assert response.status_code == 200
    assert response.json() == {"available_languages": [{"language_code": "en"}]}


def test_invalid_url_error_remains_clear():
    response = client.post("/video-captions", json={"url": "https://example.com/nope"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid YouTube URL"
