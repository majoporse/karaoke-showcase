# 📚 Song Management Service

The persistence layer and database coordinator for Karaoke-Inator. Manages song metadata, processing results, lyrics storage, and full-text search—enabling users to find and retrieve songs they've processed.

## Overview

The Song Management Service implements a Clean Architecture pattern, separating concerns into domain models, business logic, and API layers. It provides CRUD operations for songs, search capabilities via Elasticsearch, and manages the relationship between songs, versions, processing results, and lyrics.

## Core Responsibilities

### 💾 Data Persistence
Stores song metadata (title, artist, album, year) and processing results in PostgreSQL with ACID guarantees.

### 🔍 Full-text Search
Indexes lyrics and metadata in Elasticsearch for fast, relevant song discovery across the entire catalog.

### 📋 Result Management
Associates voice separation and lyrics extraction results with specific song versions, tracking processing status and timestamps.

### 🏗️ Domain Modeling
Implements business entities (Song, ProcessingResult, Lyrics) with clear boundaries and responsibilities.

### 🔗 Relationship Management
Manages complex relationships between songs, versions, processing results, and lyrics chunks.

## Technology Stack

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Async web framework |
| **Python 3.12** | Production-grade environment |
| **SQLAlchemy 2.0** | Async ORM with async support |
| **PostgreSQL 18** | Primary relational database |
| **asyncpg** | Async PostgreSQL driver |
| **Alembic** | Database schema migrations |
| **Elasticsearch 8** | Full-text search engine |
| **Pydantic 2** | Data validation and serialization |
| **Dishka** | Dependency injection |
| **OpenTelemetry** | Tracing and observability |

## Architecture Pattern: Clean Architecture

```
api/           - FastAPI routes & HTTP contracts
├── routes/
│   ├── songs.py        - Song CRUD endpoints
│   ├── search.py       - Search endpoints
│   ├── results.py      - Processing results
│   └── lyrics.py       - Lyrics retrieval

services/      - Business logic & use cases
├── song_service.py     - Song operations
├── search_service.py   - Search coordination
└── result_service.py   - Processing result handling

domain/        - Business entities (core logic)
├── song.py             - Song entity
├── processing_result.py - Processing entity
└── lyrics.py           - Lyrics entity

infrastructure/ - External dependencies
├── postgres.py         - PostgreSQL implementation
├── elasticsearch_impl.py - Elasticsearch implementation
└── models.py           - SQLAlchemy ORM models
```

**Advantages:**
- Domain logic independent of frameworks
- Easy to test (mock dependencies)
- Framework-agnostic entities
- Clear separation of concerns

## Data Models

### Song Entity
```python
class Song:
    id: str
    title: str
    artist: str
    album: Optional[str]
    year: Optional[int]
    duration: int         # seconds
    source_url: str       # YouTube URL
    versions: List[SongVersion]
    created_at: datetime
    updated_at: datetime
```

### Processing Result
```python
class ProcessingResult:
    id: str
    song_version_id: str
    status: str           # "processing", "completed", "failed"
    voice_url: str        # MinIO presigned URL
    accompaniment_url: str
    zip_url: str
    started_at: datetime
    completed_at: Optional[datetime]
    error: Optional[str]
```

### Lyrics
```python
class Lyrics:
    id: str
    processing_result_id: str
    full_text: str
    language: str
    chunks: List[LyricsChunk]
    
class LyricsChunk:
    timestamp: float      # seconds
    text: str
    confidence: float     # 0-1
```

## API Endpoints

### Song CRUD

**POST** `/api/songs`
- Create new song record

```json
{
  "title": "Song Title",
  "artist": "Artist Name",
  "album": "Album Name",
  "year": 2024,
  "duration": 180,
  "source_url": "https://youtube.com/..."
}
```

**GET** `/api/songs/{id}`
- Retrieve complete song with versions, results, and lyrics

**GET** `/api/songs`
- List all songs with pagination

**PUT** `/api/songs/{id}`
- Update song metadata

**DELETE** `/api/songs/{id}`
- Delete song and all associated data

### Search

**GET** `/api/search`
- Full-text search across songs and lyrics

```json
{
  "query": "Beatles",
  "limit": 20,
  "offset": 0,
  "filter": {
    "artist": "Beatles",
    "year_min": 1960,
    "year_max": 1970
  }
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "song123",
      "title": "Hey Jude",
      "artist": "The Beatles",
      "album": "Hey Jude",
      "year": 1968,
      "highlights": "...famous <em>Beatles</em> track..."
    }
  ],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

### Processing Results

**GET** `/api/songs/{id}/results`
- Get all processing results for a song

**POST** `/api/results`
- Create new processing result record

```json
{
  "song_version_id": "version123",
  "status": "completed",
  "voice_url": "minio://...",
  "accompaniment_url": "minio://..."
}
```

### Lyrics

**GET** `/api/songs/{id}/lyrics`
- Get lyrics for a song with timestamps

**POST** `/api/lyrics`
- Store extracted lyrics

```json
{
  "processing_result_id": "result123",
  "full_text": "Extracted lyrics...",
  "language": "en",
  "chunks": [
    { "timestamp": 0.0, "text": "Word", "confidence": 0.95 }
  ]
}
```

## Database Schema

### Tables

**songs**
```sql
CREATE TABLE songs (
  id UUID PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  artist VARCHAR(255) NOT NULL,
  album VARCHAR(255),
  year INTEGER,
  duration INTEGER,
  source_url VARCHAR(2000) UNIQUE,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

**song_versions**
```sql
CREATE TABLE song_versions (
  id UUID PRIMARY KEY,
  song_id UUID REFERENCES songs(id),
  version_type VARCHAR(50),  -- ORIGINAL, COVER, REMIX, LIVE
  created_at TIMESTAMP
);
```

**processing_results**
```sql
CREATE TABLE processing_results (
  id UUID PRIMARY KEY,
  song_version_id UUID REFERENCES song_versions(id),
  status VARCHAR(50),
  voice_url VARCHAR(2000),
  accompaniment_url VARCHAR(2000),
  zip_url VARCHAR(2000),
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  error TEXT
);
```

**lyrics**
```sql
CREATE TABLE lyrics (
  id UUID PRIMARY KEY,
  processing_result_id UUID REFERENCES processing_results(id),
  full_text TEXT,
  language VARCHAR(10),
  created_at TIMESTAMP
);
```

**lyrics_chunks**
```sql
CREATE TABLE lyrics_chunks (
  id UUID PRIMARY KEY,
  lyrics_id UUID REFERENCES lyrics(id),
  timestamp FLOAT,
  text VARCHAR(500),
  confidence FLOAT
);
```

## Elasticsearch Integration

### Indexing Strategy
Songs and lyrics are indexed in Elasticsearch for fast full-text search:

```json
{
  "index": "karaoke_songs",
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "artist": { "type": "text" },
      "lyrics": { "type": "text" },
      "album": { "type": "keyword" },
      "year": { "type": "integer" },
      "created_at": { "type": "date" }
    }
  }
}
```

### Search Capabilities
- Phrase matching: `"hey jude"`
- Fuzzy matching: `beatles` matches "Beatles"
- Relevance scoring for ranking results

## Configuration

### Environment Variables
```bash
# PostgreSQL
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=karaoke
POSTGRES_PASSWORD=password
POSTGRES_DB=karaoke_db

# Elasticsearch
ELASTICSEARCH_HOST=elasticsearch
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_INDEX_PREFIX=karaoke

# API
SERVICE_PORT=8003
LOG_LEVEL=INFO

# Search
SEARCH_TIMEOUT_SECONDS=5
MAX_SEARCH_RESULTS=1000
```

### Database Migrations with Alembic

Initialize migrations:
```bash
alembic init alembic
```

Create migration:
```bash
alembic revision --autogenerate -m "Add songs table"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback:
```bash
alembic downgrade -1
```

## Development

### Prerequisites
```bash
# Python 3.12
# PostgreSQL running locally
# Elasticsearch running locally
```

### Running Locally

```bash
cd services/song-management-service

# Install dependencies
uv sync

# Run database migrations
uv run alembic upgrade head

# Start the service
uv run python main.py
```

### File Structure
```
song-management-service/
├── main.py                 # FastAPI application
├── pyproject.toml          # Dependencies
├── alembic/                # Database migrations
├── api/
│   ├── routes.py           # API endpoints
│   └── schemas.py          # Request/response schemas
├── domain/
│   ├── song.py             # Song entity
│   ├── processing_result.py # Processing result entity
│   └── lyrics.py           # Lyrics entity
├── services/
│   ├── song_service.py     # Song business logic
│   ├── search_service.py   # Search logic
│   └── result_service.py   # Processing result logic
├── infrastructure/
│   ├── postgres.py         # PostgreSQL repository
│   ├── elasticsearch_impl.py # Elasticsearch service
│   └── models.py           # SQLAlchemy ORM
├── config.py               # Configuration
└── di.py                   # Dependency injection
```

### Type Checking
```bash
uv run pyright .
```

### Running Tests
```bash
uv run pytest tests/
```

## Production Deployment

### Docker
```bash
# Build image
docker build -t song-management-service .
docker run -p 8003:8003 song-management-service
```

### Database Backup & Recovery
```bash
# Backup
pg_dump -U karaoke karaoke_db > backup.sql

# Restore
psql -U karaoke karaoke_db < backup.sql
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: song-management
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: song-management
        image: song-management-service:latest
        resources:
          requests:
            memory: "1Gi"
            cpu: "1"
          limits:
            memory: "2Gi"
            cpu: "2"
```

### Connection Pooling
Uses SQLAlchemy's connection pooling for efficient database access:

```python
# Configured in config.py
pool_size=20          # Connections to keep open
max_overflow=10       # Additional connections when needed
pool_recycle=3600     # Recycle connections every hour
```

## Performance Optimization

### Indexing
Database indexes on frequently searched columns:
```sql
CREATE INDEX idx_songs_artist ON songs(artist);
CREATE INDEX idx_songs_title ON songs(title);
CREATE INDEX idx_songs_year ON songs(year);
```

### Elasticsearch Sharding
Multiple shards for parallel search:
```json
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1
  }
}
```

### Query Optimization
- Lazy loading relationships
- Pagination to limit result sets
- Database-level filtering before Python processing
- Connection pooling for reuse

## Monitoring & Observability

### Prometheus Metrics
- Query execution time
- Search latency
- Database connection pool stats
- Elasticsearch index health

### Alarms
- High query latency (>1s)
- Database connection pool exhaustion
- Elasticsearch unavailability
- Migration failures

## Troubleshooting

### Database Connection Issues
1. Check PostgreSQL is running: `psql -U karaoke -d karaoke_db`
2. Verify credentials in `.env`
3. Check network connectivity to database
4. Review connection pool settings

### Elasticsearch Connection
1. Test connectivity: `curl http://elasticsearch:9200`
2. Check index existence: `curl http://elasticsearch:9200/karaoke_songs`
3. Verify mapping: `curl http://elasticsearch:9200/karaoke_songs/_mapping`

### Search Returning No Results
1. Verify index is populated: `curl http://elasticsearch:9200/karaoke_songs/_count`
2. Check query syntax
3. Review search relevance scoring
4. Try simpler query without special characters

### Slow Queries
1. Check database indexes: `SELECT * FROM pg_stat_user_indexes`
2. Review query plans: `EXPLAIN ANALYZE SELECT ...`
3. Add missing indexes
4. Check connection pool utilization

---

**For system architecture**, see [README.md](../README.md) or [BLOG.md](../BLOG.md).

**For orchestrator/coordination**, check [orchestrator-service/README.md](../orchestrator-service/README.md).
