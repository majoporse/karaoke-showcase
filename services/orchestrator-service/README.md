# 🎛️ Orchestrator Service

Central API gateway for Karaoke-Inator that manages the karaoke processing pipeline. Handles YouTube audio download, coordinates parallel voice separation and lyrics extraction, stores results in MinIO, and provides real-time WebSocket updates.

## Key Features

- **YouTube Audio Download**: yt-dlp extracts audio from YouTube URLs with proxy support
- **Distributed Job Queue**: RQ + Redis for parallel processing with multiple workers
- **Real-time Updates**: WebSocket for live progress streaming and reconnection support
- **Result Storage**: MinIO for audio files, PostgreSQL for metadata (via Song Management Service)
- **Search**: Full-text search across lyrics via Song Management Service

## Technology Stack

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Async Python web framework |
| **Python 3.12** | Latest Python with performance improvements |
| **RQ (Redis Queue)** | Distributed job queue |
| **Redis** | Job queue, pub/sub, caching |
| **yt-dlp** | YouTube audio downloader |
| **MinIO** | S3-compatible object storage for audio files |
| **PostgreSQL** | Metadata persistence (via Song Management Service) |
| **WebSockets** | Real-time progress updates |

## API Endpoints

### Processing

**POST** `/process/queue`
Submit YouTube URL for processing.
```json
Request: { "youtube_url": "https://www.youtube.com/watch?v=..." }
Response: { "job_id": "abc123" }
```

**GET** `/process/processing/{id}`
Get song processing result by ID (vocals path, accompaniment path, lyrics).

**GET** `/process/search?query=beatles&limit=10&page=0`
Search processed songs by lyrics query.

### Queue & Progress

**GET** `/process/queue/position/{task_id}`
Get task queue position.

**GET** `/process/job/{job_id}/latest-message`
Get latest progress message (for client reconnection).

### Storage

**GET** `/presign?key=songs/uuid/vocals.mp3`
Get presigned MinIO URL for direct file access.

### Health

**GET** `/health`
Health check for orchestrator and dependent services.

### WebSocket

**WS** `/ws/progress`
Real-time job progress updates via Redis pub/sub.

## Processing Pipeline

1. **YouTube Download**: Validate URL → Extract audio with yt-dlp → Convert to WAV → Save to MinIO
2. **Parallel Processing** (concurrent):
   - Voice Separation Service: Outputs vocals + accompaniment to MinIO
   - Lyrics Extraction Service: Outputs lyrics + word-level timestamps
3. **Result Storage**: Save MinIO paths and lyrics to PostgreSQL via Song Management Service
4. **Client Notification**: Send completion via WebSocket with all results

## Configuration

### Environment Variables

```bash
# Services
VOICE_SEPARATION_URL=http://voice-separation:8001
LYRICS_EXTRACTION_URL=http://lyrics-extraction:8002
SONG_MANAGEMENT_URL=http://song-management:8003

# Redis & Job Queue
REDIS_URL=redis://redis:6379/0

# MinIO Storage
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_SECURE=false
MINIO_BUCKET_NAME=karaoke

# yt-dlp Configuration
YOUTUBE_PO_TOKEN=                    # Optional: PO token for age-restricted videos
YOUTUBE_COOKIES_PATH=                # Optional: Cookies file for authenticated downloads
PROXY_URL=                           # Optional: Proxy for YouTube requests (http://proxy:8080 or socks5://proxy:1080)
POT_URL=                             # Optional: Custom PO token server
SERVER_URL=                          # Optional: For minio signing

# API
ORCHESTRATOR_PORT=8000
LOG_LEVEL=INFO
```

## Data Models

### Processing Result
```python
class ProcessingResult(BaseModel):
    success: bool
    vocals_path: Optional[str]              # MinIO path: songs/uuid/vocals.mp3
    accompaniment_path: Optional[str]       # MinIO path: songs/uuid/accompaniment.mp3
    lyrics: Optional[str]                   # Full transcribed text
    chunks: Optional[List[Chunk]]           # Word-level timing
    yt_metadata: Optional[YouTubeVideoMetadata]
    error: Optional[str]

class Chunk(BaseModel):
    start: float    # Seconds
    end: float      # Seconds
    text: str       # Lyrics for this segment
```

### WebSocket Message
```python
class ProcessingOutputPayload(BaseModel):
    current_step: int       # 0-5
    total_steps: int        # Always 5
    desc: str              # Status message
    result: Optional[ProcessingResult]  # Populated on completion/error
```

## Background Jobs (RQ)

Jobs are enqueued to Redis and processed by workers:

```bash
# Start a worker (processes jobs from "default" queue)
uv run rq worker default
```

**Redis Usage:**
- Job queue storage (RQ)
- Pub/sub for progress updates (WebSocket subscriptions)
- Message caching (1-hour expiration for client reconnection)

## Development

### Prerequisites
- Python 3.12
- Redis (localhost:6379)
- Voice Separation service (localhost:8001)
- Lyrics Extraction service (localhost:8002)
- Song Management service (localhost:8003)
- MinIO (localhost:9000)

### Setup & Run

```bash
cd services/orchestrator-service

# Install dependencies
uv sync

# Run service
uv run python -m main

# In another terminal, start worker
uv run rq worker default

# Type checking
uv run pyright .
```

### Directory Structure

```
orchestrator-service/
├── main.py                  # FastAPI entry point
├── config.py                # Configuration from env vars
├── routes/                  # API endpoints
│   ├── processing.py        # /process endpoints
│   ├── sign_storage.py      # /presign endpoint
│   └── ws.py                # WebSocket endpoints
├── services/                # Business logic
│   ├── orchestrator_service.py     # Main orchestration
│   ├── youtube_downloader.py       # YouTube audio download
│   ├── voice_separation_service.py # Voice separation calls
│   ├── lyrics_extraction_service.py# Lyrics extraction calls
│   ├── song_management_service.py  # Song Management API calls
│   └── minio_service.py            # MinIO client wrapper
├── tasks/                   # RQ job definitions
│   ├── audio_processing_job.py     # Main processing pipeline
│   └── queue_tasks.py              # Queue + pub/sub utilities
├── models/                  # Pydantic models
└── clients/                 # Auto-generated service clients
```

## Deployment

### Docker

```bash
docker build -t orchestrator-service .
docker run -p 8000:8000 orchestrator-service

docker build -t rq-worker -f worker/Dockerfile .
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Jobs not processing | Check Redis: `redis-cli ping`, Check workers: `rq info` |
| Service communication fails | Verify service URLs in config, check service health endpoints |
| WebSocket connection drops | Check network stability, verify firewall allows persistent connections |
| High memory usage | Set worker max-jobs: `rq worker --max-jobs 100` |

---

For system-wide architecture, see [project README](../README.md).
