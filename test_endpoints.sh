#!/usr/bin/env bash
set -euo pipefail

SERVER_URL="${1:-http://localhost:8000}"
VIDEO_URL="${2:-https://www.youtube.com/watch?v=dQw4w9WgXcQ}"
SHORT_URL="https://youtu.be/dQw4w9WgXcQ"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-30}"

request() {
  local method="$1"
  local path="$2"
  local body="${3:-}"

  echo
  echo "$method $path"
  if [[ "$method" == "GET" ]]; then
    curl -sS --max-time "$TIMEOUT_SECONDS" -X "$method" "$SERVER_URL$path" | python3 -m json.tool
  else
    curl -sS --max-time "$TIMEOUT_SECONDS" -X "$method" "$SERVER_URL$path" \
      -H "Content-Type: application/json" \
      -d "$body" | python3 -m json.tool
  fi
}

request GET /health
request POST /video-data "{\"url\":\"$VIDEO_URL\"}"
request POST /youtube/video-data "{\"url\":\"$SHORT_URL\"}"
request POST /video-transcript-languages "{\"url\":\"$VIDEO_URL\"}"
request POST /youtube/video-transcript-languages "{\"url\":\"$VIDEO_URL\"}"
request POST /video-captions "{\"url\":\"$VIDEO_URL\",\"languages\":[\"en\"]}"
request POST /youtube/video-captions "{\"url\":\"$VIDEO_URL\",\"languages\":[\"en\"]}"
request POST /video-timestamps "{\"url\":\"$VIDEO_URL\",\"languages\":[\"en\"]}"
request POST /youtube/video-timestamps "{\"url\":\"$VIDEO_URL\",\"languages\":[\"en\"]}"

echo
echo "Expected invalid-url failure:"
curl -sS --max-time "$TIMEOUT_SECONDS" -X POST "$SERVER_URL/video-captions" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/not-youtube"}' | python3 -m json.tool

echo
echo "Endpoint checks completed."
