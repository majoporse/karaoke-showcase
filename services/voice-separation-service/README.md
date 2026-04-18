# 🔊 Voice Separation Service

Isolates vocals from musical accompaniment using deep learning models. This specialized service receives raw audio and returns separated vocal and instrumental tracks ready for karaoke playback.

## Overview

The Voice Separation Service is the core of the vocal isolation feature. It uses state-of-the-art neural network models trained to understand audio source separation—the task of decomposing mixed audio into individual instruments and vocals. This service runs independently from the orchestrator, enabling horizontal scaling for parallel song processing.

## How It Works

### The Separation Process
1. **Retrieve Audio** - Fetches raw audio from MinIO by object path
2. **Preprocess** - Normalizes audio format, sample rate, and channels
3. **Model Inference** - Runs deep learning model to identify and separate sources
4. **Extract Stems** - Isolates vocals and accompaniment tracks
5. **Compress** - Encodes separated tracks to MP3 format
6. **Store Results** - Uploads vocals and accompaniment to MinIO, returns object paths

### Supported Models

| Model | Speed | Quality | CPU/GPU | Best For |
|-------|-------|---------|---------|----------|
| **Demucs** | Medium | High | GPU | Professional use |
| **Spleeter** | Fast | Medium | CPU | Quick processing |

**Demucs** (Facebook's source separation):
- Deep convolutional neural network
- Trained on multiple datasets
- Superior vocal/accompaniment separation
- Higher computational cost

**Spleeter** (Deezer's model):
- Faster inference speed
- Works well on CPU
- Good enough for most use cases
- Lower latency

## Core Features

### Audio Format Support
Accepts any format supported by FFmpeg:
- WAV, MP3, FLAC, OGG, M4A, AAC, and more
- Automatically handles codec conversion
- Resamples to optimal processing rate (44.1 kHz or 48 kHz)

### Output Formats
- **Vocals**: Isolated vocal track as MP3 file
- **Accompaniment**: Instrumental-only track as MP3 file
- **Storage**: Both files uploaded to MinIO object storage
- **Access**: Client receives MinIO object paths for retrieval

### Quality Indicators
The response includes paths to the separated audio files in MinIO storage. Clients can fetch these files and use them for:
- Karaoke playback (vocals)
- Background music (accompaniment)
- Lyrics extraction (from vocals track)

## Technology Stack

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Async web framework |
| **Python 3.10** | Stable ML/audio environment |
| **PyTorch** | Deep learning framework |
| **Demucs** | Facebook's source separation model |
| **Spleeter** | Deezer's separation model |
| **librosa** | Audio analysis and feature extraction |
| **soundfile** | Audio file I/O |
| **numpy** | Numerical computing for audio processing |
| **FFmpeg** | Audio codec handling |
| **MinIO SDK** | Result storage in S3 |

## API Endpoints

### Voice Separation

**POST** `/separate-voice`
- Retrieve audio from MinIO by object path, perform separation, and store results
- Takes MinIO object path as input, returns paths to separated audio files in MinIO

```json
// Request
{
  "minio_path": "songs/audio-abc123.wav"
}

// Response
{
  "vocals_path": "tmp/vocals-abc123.mp3",
  "accompaniment_path": "tmp/accompaniment-abc123.mp3"
}
```

### Configuration Information

**GET** `/separate-voice/config`
- Returns information about available models and current configuration

```json
{
  "active_model": "demucs",
  "available_models": {
    "demucs": {
      "description": "Facebook's Demucs model - highest quality separation",
      "memory_efficient": false,
      "quality": "high",
      "supported_formats": ["mp3", "wav", "m4a", "flac", "ogg"]
    },
    "spleeter": {
      "description": "Deezer's Spleeter model - fast and efficient separation",
      "memory_efficient": true,
      "quality": "medium",
      "supported_formats": ["mp3", "wav", "m4a", "flac"]
    }
  }
}
```

### Service Health

**GET** `/health`
- Check service status and model availability

```json
{
  "status": "healthy",
  "models_loaded": ["demucs", "spleeter"],
  "gpu_available": false,
  "memory_usage_mb": 2048
}
```

## Model Management

### MinIO Integration

Audio files and separation results are stored in **MinIO**, an S3-compatible object storage service. This enables:

- **Distributed Processing**: Multiple workers can access the same audio files
- **Scalable Storage**: Handles large audio files without local disk constraints
- **Easy Retrieval**: Clients get object paths for direct access
- **Efficient Workflow**: Results immediately available to downstream services

**How it works:**
1. Orchestrator uploads raw audio to MinIO → stores path
2. Voice Separation Service fetches audio by path
3. Separates vocals and accompaniment
4. Uploads compressed MP3 files back to MinIO → returns paths
5. Downstream services (lyrics extraction, karaoke player) access results via MinIO paths

**MinIO Configuration:**
```bash
MINIO_ENDPOINT=minio:9000          # MinIO server address
MINIO_BUCKET=karaoke               # Bucket for audio files
MINIO_ACCESS_KEY=minioadmin        # S3 access key
MINIO_SECRET_KEY=minioadmin        # S3 secret key
MINIO_SECURE=false                 # Use HTTPS (false for local/docker)
```

### Model Caching
Models are downloaded and cached on first use. Subsequent requests use cached models for faster performance.

- **Demucs**: ~1.5 GB
- **Spleeter**: ~1.2 GB

Cache location: `~/.cache/torch/` and `~/.cache/spleeter/`

### GPU Support
GPU acceleration available for NVIDIA GPUs:

```bash
# With GPU (CUDA 12.8)
docker build -f Dockerfile.gpu -t voice-separation .

# CPU-only (default)
docker build -t voice-separation .
```

GPU provides ~5-10x speedup for separation.

## Performance Characteristics

### Processing Time
- **Demucs (GPU)**: 10-30 seconds for 3-minute song
- **Demucs (CPU)**: 30-60 seconds for 3-minute song
- **Spleeter (CPU)**: 20-40 seconds for 3-minute song

### Memory Requirements
- **Base**: ~500 MB RAM
- **Demucs loaded**: +1.5 GB
- **Active separation**: +500 MB (audio buffer)
- **GPU VRAM**: 2-4 GB for GPU acceleration

### Throughput
With single worker:
- 1 song per 45 seconds (average, CPU)
- 1 song per 25 seconds (average, GPU)

Scales linearly with additional workers.

## Configuration

### Environment Variables
```bash
# Model selection
VOICE_SEPARATION_MODEL=demucs  # or spleeter
VOICE_SEPARATION_DEVICE=cpu    # or cuda, mps

# Processing
AUDIO_SAMPLE_RATE=44100
CHUNK_SIZE=262144
MAX_WORKERS=4

# MinIO storage (for results)
MINIO_ENDPOINT=minio:9000
MINIO_BUCKET=karaoke/separated
MINIO_SECURE=false

# API
SERVICE_PORT=8001
LOG_LEVEL=INFO
```

### Model Selection
Choose model based on your use case:

- **High quality needed?** → Use Demucs
- **Speed critical?** → Use Spleeter
- **Limited resources?** → Use Spleeter + CPU
- **Best experience?** → Use Demucs + GPU

## Architecture

### Input Pipeline
```
Raw Audio → Codec Detection → Resampling → Normalization → Model Input
```

### Processing
```
Audio Tensor → Demucs/Spleeter Model → Frequency Domain Analysis
→ Source Separation → Reconstruction → Audio Output
```

### Output Pipeline
```
Vocal Track → Compression to MP3 → Upload to MinIO
Accompaniment Track → Compression to MP3 → Upload to MinIO
→ Return object paths to client
```

## Development

### Prerequisites
```bash
# Python 3.10, PyTorch, FFmpeg
```

### Running Locally

```bash
cd services/voice-separation-service

# Install dependencies
uv sync

# Run the service (CPU)
uv run python main.py

# Run with GPU (if available)
VOICE_SEPARATION_DEVICE=cuda uv run python main.py
```

### File Structure
```
voice-separation-service/
├── main.py                          # FastAPI application
├── pyproject.toml                   # Dependencies
├── routes/
│   ├── unified_separation.py        # Voice separation endpoints
│   ├── health.py                    # Health check endpoint
│   └── openapi.py                   # OpenAPI schema
├── services/
│   ├── unified_separation_service.py # Orchestrates separation workflow
│   ├── minio_service.py             # MinIO S3 client wrapper
│   ├── models/
│   │   ├── base_model.py            # Base separator interface
│   │   ├── demucs_model.py          # Demucs implementation
│   │   └── spleeter_model.py        # Spleeter implementation
│   ├── compress_audio.py            # MP3 encoding
│   └── zip.py                       # Legacy ZIP utility (deprecated)
├── models/
│   ├── common.py                    # Common response models
│   └── separation.py                # Separation request/response schemas
├── config/
│   ├── settings.py                  # Environment configuration
│   └── model_config.py              # Model-specific config
└── .env.example                     # Environment template
```

### Type Checking
```bash
uv run pyright .
```

## Production Deployment

### Docker
```bash
# CPU-only image
docker build -t voice-separation .
docker run -p 8001:8001 voice-separation

# GPU-enabled image
docker build -f Dockerfile.gpu -t voice-separation:gpu .
docker run --gpus all -p 8001:8001 voice-separation:gpu
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: voice-separation
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: voice-separation
        image: voice-separation:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "2"
          limits:
            memory: "4Gi"
            cpu: "4"
      # Use GPU nodes if available
      - nodeSelector:
          accelerator: nvidia-tesla-v100
```

### Monitoring
- Prometheus metrics at `/metrics`
- Grafana dashboards for separation quality
- Model loading and inference latency tracking

## Troubleshooting

### Model Not Loading
1. Check disk space: `df -h`
2. Verify download: `ls ~/.cache/torch/`
3. Check internet: `curl -I https://huggingface.co`
4. Try manual download: See Torch documentation

### Out of Memory
1. Reduce chunk size: `CHUNK_SIZE=131072`
2. Use Spleeter instead: `VOICE_SEPARATION_MODEL=spleeter`
3. Process shorter audio files
4. Add swap space or increase RAM

### Poor Separation Quality
1. Try Demucs model if using Spleeter
2. Check audio quality (avoid heavily compressed MP3)
3. Verify sample rate normalization
4. Test with different audio sources

### GPU Not Detected
1. Check CUDA installation: `nvidia-smi`
2. Verify PyTorch GPU: `python -c "import torch; print(torch.cuda.is_available())"`
3. Install CUDA toolkit and cuDNN
4. Fall back to CPU mode

---

**For system architecture**, see [README.md](../README.md) or [BLOG.md](../BLOG.md).

**For orchestrator/coordination**, check [orchestrator-service/README.md](../orchestrator-service/README.md).
