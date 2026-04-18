# 🎼 Lyrics Extraction Service

Automatically transcribes audio to synchronized, timestamped lyrics using OpenAI's Whisper speech-to-text model. This service converts audio into readable lyrics with precise word-level timing for perfect karaoke synchronization.

## Overview

The Lyrics Extraction Service leverages Whisper, one of the most advanced speech recognition models available, to accurately transcribe vocals from audio files. Beyond simple transcription, it provides word-level timestamps enabling the frontend to synchronize lyrics display with playback in real-time.

## How It Works

### The Transcription Process
1. **Receive Audio** - Accepts raw audio bytes (any format)
2. **Preprocess Audio** - Extracts vocals if needed, normalizes levels
3. **Speech Recognition** - Whisper model identifies spoken/sung words
4. **Timestamp Generation** - Maps each word to precise audio timing
5. **Format Output** - Returns both plain text and timestamped JSON
6. **Validate Quality** - Checks transcription confidence and completeness

### Supported Languages
Whisper supports 99+ languages including:
- English, Spanish, French, German, Italian, Portuguese
- Russian, Japanese, Chinese, Korean, Arabic, Hindi
- And many more...

Auto-detects language from audio, no need to specify.

## Core Features

### Speech Recognition
- Robust to background music, crowd noise, and audio quality issues
- Handles different accents, speaking rates, and vocal styles
- Works with both spoken word and sung lyrics
- Confidence scores for each transcription

### Timestamp Accuracy
- Word-level timing (±100ms accuracy typical)
- Useful for karaoke sync and music video subtitles
- Optional phrase-level grouping
- Stability enhancement to smooth timing variations

### Multiple Output Formats

**Plain Text Lyrics:**
```
This is the first line
And this is the second line
And so on...
```

**Timestamped Lyrics:**
```json
{
  "chunks": [
    { "start": 0.0, "end": 0.5, "text": "This" },
    { "start": 0.5, "end": 0.8, "text": "is" },
    { "start": 0.8, "end": 1.2, "text": "the" },
    { "start": 1.2, "end": 1.6, "text": "first" },
    { "start": 1.6, "end": 2.1, "text": "line" }
  ],
  "text": "This is the first line",
  "total_duration_seconds": 180,
  "sample_rate": 16000
}
```

**Phrase-level:**
```json
{
  "chunks": [
    { "start": 0.0, "end": 3.0, "text": "This is the first line" },
    { "start": 3.0, "end": 6.5, "text": "And this is the second line" }
  ],
  "text": "This is the first line And this is the second line",
  "total_duration_seconds": 180,
  "sample_rate": 16000
}
```

## Technology Stack

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Async web framework |
| **Python 3.10** | ML-optimized environment |
| **PyTorch** | Deep learning framework |
| **Faster-Whisper** | Optimized Whisper inference |
| **Whisper** | OpenAI speech recognition model |
| **Stable-ts** | Timestamp stabilization |
| **librosa** | Audio analysis and preprocessing |
| **soundfile** | Audio file I/O |
| **transformers** | Hugging Face model library |
| **torchaudio** | Audio processing utilities |

## API Endpoints

### Extract Lyrics

**POST** `/extract-lyrics`
- Receive audio from MinIO storage and transcribe to plain text lyrics

```json
// Request
{
  "minio_path": "songs/audio-abc123.wav"
}

// Response
{
  "text": "Full lyrics text...",
  "duration_seconds": 180,
  "sample_rate": 16000
}
```

### Extract Lyrics with Timestamps

**POST** `/extract-lyrics/with-timestamps`
- Transcribe to word-level timestamped lyrics from MinIO-stored audio

```json
// Request
{
  "minio_path": "songs/audio-abc123.wav"
}

// Response
{
  "chunks": [
    { "start": 0.0, "end": 0.5, "text": "Word" },
    { "start": 0.5, "end": 0.8, "text": "by" },
    { "start": 0.8, "end": 1.1, "text": "word" }
  ],
  "text": "Word by word...",
  "total_duration_seconds": 180,
  "sample_rate": 16000
}
```


### Service Health

**GET** `/health`
- Check service status and model availability

```json
{
  "status": "healthy",
  "model": "base",
  "gpu_available": true,
  "memory_usage_mb": 3200
}
```

## Whisper Models

| Model | Size | Speed | Accuracy | Recommended For |
|-------|------|-------|----------|-----------------|
| **tiny** | 39 MB | Very Fast | Good | Quick testing, real-time |
| **small** | 139 MB | Fast | Very Good | Balanced use |
| **base** | 140 MB | Medium | Excellent | Production (default) |
| **medium** | 769 MB | Slow | Nearly Perfect | Challenging audio |
| **large** | 2.9 GB | Very Slow | Perfect | Archive/best quality |

Choose based on accuracy needs vs speed:
- **Low latency?** → tiny or small
- **Best accuracy?** → base or medium
- **Perfect transcription?** → large (needs GPU)

## Performance Characteristics

### Memory Requirements
- **Base model**: 400 MB loaded
- **Inference**: +300-500 MB per request
- **GPU VRAM**: 2-4 GB for GPU acceleration

### Accuracy Metrics
- Word Error Rate (WER): 5-15% depending on audio quality
- Speaker Diarization: Not supported
- Background Music: Robust to accompaniment

## Configuration

### Environment Variables
```bash
# Model selection
WHISPER_MODEL=base         # tiny, small, base, medium, large
WHISPER_DEVICE=cpu         # or cuda, mps

# Processing
LANGUAGE=null              # null = auto-detect, or language code
TIMESTAMP_GRANULARITY=word # or phrase
CONFIDENCE_THRESHOLD=0.3

# Audio preprocessing
SAMPLE_RATE=16000
TRIM_SILENCE=true
NORMALIZE_AUDIO=true

# API
SERVICE_PORT=8002
LOG_LEVEL=INFO
```

### Language Codes
Common ISO 639-1 codes:
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `ja` - Japanese
- `zh` - Chinese
- `ko` - Korean

## Architecture

### Audio Preprocessing
```
Raw Audio → Format Detection → Resampling to 16kHz
→ Silence Trimming → Normalization → Whisper Input
```

### Speech Recognition
```
Audio Waveform → Mel-Spectrogram → Whisper Encoder
→ Cross-Attention Decoder → Token Predictions → Text Output
```

### Timestamp Generation
```
Token Predictions → Alignment with Audio
→ Word-Level Timing → Stability Enhancement → Final Timestamps
```

## Development

### Prerequisites
```bash
# Python 3.10
# PyTorch (CPU or GPU)
# FFmpeg for audio handling
```

### Running Locally

```bash
cd services/lyrics-extraction-service

# Install dependencies
uv sync
cp .env.example .env

# Run the service
uv run python -m main

# With GPU (if available)
# look inside the pyproject.toml and comment out the cpu version. uncomment gpu.
```

### File Structure
```
lyrics-extraction-service/
├── main.py                 # FastAPI application
├── pyproject.toml          # Dependencies
├── routes/
│   ├── extraction.py       # Transcription endpoints
│   └── models.py           # Model information
├── services/
│   ├── whisper_service.py  # Whisper wrapper
│   ├── timestamp_service.py# Timestamp generation
│   └── audio_service.py    # Audio preprocessing
├── config.py               # Configuration
└── models/                 # Pydantic models
```

### Type Checking
```bash
uv run pyright .
```

## Production Deployment

### Docker
```bash
# CPU-only image
docker build -t lyrics-extraction .
docker run -p 8002:8002 lyrics-extraction
```

### Monitoring
- Prometheus metrics at `/metrics`
- Transcription accuracy tracking
- Processing latency by model size
- Language distribution analysis

## Troubleshooting

### Model Download Fails
1. Check internet connection
2. Verify disk space: `df -h`
3. Check Hugging Face connectivity
4. Try smaller model: `WHISPER_MODEL=tiny`

### Poor Transcription Quality
1. Improve audio quality (reduce background music)
2. Use larger model: `WHISPER_MODEL=base` or `medium`
3. Check language detection is correct
4. Test with different audio samples


### Out of Memory
1. Switch to smaller model: `WHISPER_MODEL=tiny`
2. Use CPU instead of GPU
3. Reduce batch processing
4. Increase swap space

## Use Cases

### Karaoke Synchronization
Perfect word-level timestamps enable real-time lyrics display that stays synchronized with music playback.

### Music Video Subtitles
Automatically generate subtitles with precise timing for video content.

### Accessibility
Provides transcription for hearing-impaired users while maintaining timing.

### Lyric Research
Accurate transcription useful for lyric databases and music analysis.

---

**For system architecture**, see [README.md](../README.md) or [BLOG.md](../BLOG.md).

**For orchestrator/coordination**, check [orchestrator-service/README.md](../orchestrator-service/README.md).
