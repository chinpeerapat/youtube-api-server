# YouTube API Server

A FastAPI-based server providing API endpoints for extracting and processing YouTube video data, including metadata, captions, and timestamps.

## Features

- Extract video metadata using YouTube's oEmbed API
- Retrieve video captions/transcripts
- Generate timestamped captions
- RESTful API with Swagger/OpenAPI documentation
- Docker support for easy deployment

## Requirements

- Python 3.8+
- FastAPI
- youtube-transcript-api
- Docker (optional)

## Installation

### Using Python

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd youtube-api-server
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

5. Run the server:
   ```bash
   python -m app.main
   ```

### Using Docker

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd youtube-api-server
   ```

2. Build and start the Docker container:
   ```bash
   docker-compose up -d
   ```

## Usage

Once the server is running, you can access:

- API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

### API Endpoints

#### 1. Get Video Metadata

```
POST /youtube/video-data
```

Request body:
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

Response:
```json
{
  "title": "Video Title",
  "author_name": "Channel Name",
  "author_url": "https://www.youtube.com/channel/...",
  "type": "video",
  "height": 113,
  "width": 200,
  "version": "1.0",
  "provider_name": "YouTube",
  "provider_url": "https://www.youtube.com/",
  "thumbnail_url": "https://i.ytimg.com/vi/..."
}
```

#### 2. Get Video Captions

```
POST /youtube/video-captions
```

Request body:
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "languages": ["en"]
}
```

Response:
```
"Text of the captions..."
```

#### 3. Get Video Timestamps

```
POST /youtube/video-timestamps
```

Request body:
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "languages": ["en"]
}
```

Response:
```json
[
  "0:00 - Caption at the beginning",
  "0:05 - Next caption",
  "0:10 - Another caption"
]
```

## Project Structure

```
youtube-api-server/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application initialization
│   ├── models/                # Pydantic models
│   │   ├── __init__.py
│   │   └── youtube.py
│   ├── routes/                # API routes
│   │   ├── __init__.py
│   │   └── youtube.py
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       └── youtube_tools.py
├── .env.example               # Example environment variables
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
└── docker-compose.yml         # Docker Compose configuration
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
