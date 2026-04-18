# Karaoke-Inator

Transform YouTube songs into professional karaoke tracks via a distributed microservices architecture.

## Features

- **Voice Separation** - AI-powered audio demixing (Demucs/Spleeter)
- **Lyrics Extraction** - Synchronized lyrics via OpenAI Whisper
- **Interactive Player** - Real-time playback with synced lyrics
- **Full-text Search** - Song discovery with filtering and pagination
- **Real-time Progress** - WebSocket updates for job tracking
- **Scalable Microservices** - Containerized, production-ready architecture

## Workflow

1. User uploads a YouTube URL
2. **Orchestrator Service** coordinates the pipeline
3. **Voice Separation Service** demixes vocals from instrumentals
4. **Lyrics Extraction Service** transcribes and timestamps lyrics
5. **Song Management Service** stores metadata and tracks
6. **Interactive Player** delivers synchronized playback experience

## Architecture

```
Frontend (React)
    ↓
Orchestrator Service (Port 8000)
    ├── Voice Separation (8001)
    ├── Lyrics Extraction (8002)
    ├── Song Management (8003)
    └── Data Layer (PostgreSQL, Redis, MinIO)
```

## Tech Stack

- **Frontend**: React 19, React Router 7, TypeScript
- **Backend**: FastAPI (Python 3.12)
- **AI/ML**: PyTorch, Whisper, Demucs, Spleeter
- **Data**: PostgreSQL, Redis, MinIO, Elasticsearch

## Getting Started

**Prerequisites**: Docker, Node.js 18+, 10+ GB disk space

```bash
# Clone & start backend
git clone <repo-url> && cd karaoke-inator
docker-compose up -d

# Start frontend (new terminal)
cd services/frontend
npm install && npm run dev
```

Open http://localhost:5173

## Development

See [AGENTS.md](AGENTS.md) for detailed developer guidelines, build commands, and coding standards.

**Quick commands:**

- **Frontend**: `npm run dev`, `npm run typecheck`, `npm run lint`
- **Services**: `uv sync`, `uv run python main.py`, `uv run pyright .`

## Deployment

```bash
docker-compose up -d                                    # Development
docker-compose -f docker-compose.otel.yml up -d        # With observability
docker-compose -f docker-compose.prod.certbot.yml up -d # Production
helm install karaoke-inator ./helm --namespace karaoke  # Kubernetes
```

## Documentation

- [AGENTS.md](AGENTS.md) - Developer guidelines & coding standards
- Service READMEs in `services/*/`

## License

Portfolio & demonstration purposes
