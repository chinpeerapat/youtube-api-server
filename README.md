# YouTube API Server

A FastAPI service for reading public YouTube video metadata, captions, timestamped transcripts, and available transcript languages.

The server is designed for small apps, internal tools, automations, and agents that need a simple HTTP API around YouTube oEmbed and transcript data.

## Features

- Video metadata lookup through YouTube oEmbed.
- Caption extraction with language fallback.
- Timestamped transcript generation.
- Transcript language discovery.
- Two endpoint styles: root routes and `/youtube/*` namespaced routes.
- Optional Webshare proxy support for transcript requests.
- Optional generic HTTP proxy support for metadata requests.
- Optional API key or JWT authentication.
- Docker, pytest, and curl-based endpoint checks.

## Requirements

- Python 3.10+; Python 3.12 is recommended for deploys
- `pip`
- Docker, optional

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Check the active configuration:

```bash
python load_env.py
```

## Running

Start the server locally:

```bash
python -m app.main
```

The default server address is `http://localhost:8000`.

Start with Docker:

```bash
docker-compose up -d
```

Hosted Python platforms can use the included `Procfile` and `runtime.txt`.

## API

Health and documentation:

- `GET /`
- `GET /health`
- `GET /docs`
- `GET /redoc`

Video endpoints:

- `POST /video-data`
- `POST /video-captions`
- `POST /video-timestamps`
- `POST /video-transcript-languages`
- `POST /youtube/video-data`
- `POST /youtube/video-captions`
- `POST /youtube/video-timestamps`
- `POST /youtube/video-transcript-languages`

Request body:

```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "languages": ["en", "es"]
}
```

`languages` is optional. Transcript requests try the requested languages first, then English if available, then the first available transcript language.

Example responses:

```json
{
  "title": "Video Title",
  "author_name": "Channel Name",
  "author_url": "https://www.youtube.com/@channel",
  "type": "video",
  "thumbnail_url": "https://i.ytimg.com/vi/example/hqdefault.jpg"
}
```

```json
{
  "captions": "Transcript text..."
}
```

```json
{
  "timestamps": ["0:00 - Intro", "0:05 - Next line"]
}
```

```json
{
  "available_languages": [
    {
      "language": "English",
      "language_code": "en",
      "is_generated": false,
      "is_translatable": true
    }
  ]
}
```

The `/youtube/video-captions`, `/youtube/video-timestamps`, and `/youtube/video-transcript-languages` routes return the raw captions string, timestamp list, and language list directly.

## Configuration

Server settings:

- `HOST`, default `0.0.0.0`
- `PORT`, default `8000`
- `RELOAD`, default `false`
- `LOG_LEVEL`, default `INFO`
- `BACKEND_CORS_ORIGINS`, comma-separated origins, default `*`

Generic HTTP proxy for metadata/oEmbed requests:

- `ENABLE_PROXY`
- `PROXY_TYPE`
- `PROXY_HOST`
- `PROXY_PORT`
- `PROXY_USERNAME`
- `PROXY_PASSWORD`

Webshare proxy for transcript requests:

- `WEBSHARE_PROXY_USERNAME`
- `WEBSHARE_PROXY_PASSWORD`
- `WEBSHARE_PROXY_LOCATIONS`, comma-separated, default `de,us`

Authentication is disabled by default:

- `ENABLE_AUTH=false`
- `AUTH_TYPE=api_key` or `jwt`
- `API_KEY`
- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`

When `ENABLE_AUTH=true`, video endpoints require either `X-API-Key` for API key auth or `Authorization: Bearer <token>` for JWT auth. `/`, `/health`, `/docs`, and `/redoc` remain public.

## Examples

Health check:

```bash
curl -X GET "http://localhost:8000/health"
```

Get captions:

```bash
curl -X POST "http://localhost:8000/video-captions" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ","languages":["en"]}'
```

List transcript languages:

```bash
curl -X POST "http://localhost:8000/youtube/video-transcript-languages" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

Use API key auth:

```bash
curl -X POST "http://localhost:8000/video-data" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

## Testing

Run unit and API tests:

```bash
python -m pytest
```

Run endpoint checks against a running server:

```bash
./test_endpoints.sh http://localhost:8000
```

## Project Structure

```text
youtube-api-server/
+-- app/
|   +-- core/config.py
|   +-- main.py
|   +-- middleware/
|   +-- models/youtube.py
|   +-- routes/youtube.py
|   +-- utils/youtube_tools.py
+-- tests/
+-- Dockerfile
+-- docker-compose.yml
+-- load_env.py
+-- requirements.txt
+-- test_endpoints.sh
```
