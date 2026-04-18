import asyncio
import logging
import time
from io import BytesIO

from fastapi import APIRouter, File, HTTPException, UploadFile

from components.faster_whisper_extractor import FasterWhisperExtractor
from components.minio_service import MinIOService
from config.settings import settings
from models.common import ErrorResponse
from models.lyrics import (
    LyricsExtractionResponse,
    LyricsWithTimestampsResponse,
    TranscriptionResult,
)

logger = logging.getLogger(__name__)

# Initialize router with prefix and tags
lyrics_router = APIRouter(
    prefix="/extract-lyrics",
    tags=["Lyrics Extraction"],
)

extractor = FasterWhisperExtractor()
extractor.initialize_model()
# extractor = None


@lyrics_router.post(
    "",
    response_model=LyricsExtractionResponse,
    summary="Extract plain lyrics",
    description="Extract lyrics as plain text from an audio file using Whisper speech recognition",
    responses={
        200: {
            "description": "Lyrics extracted successfully",
            "model": LyricsExtractionResponse,
        },
        400: {
            "description": "Invalid file type (not an audio file)",
            "model": ErrorResponse,
        },
        500: {"description": "Error processing audio file", "model": ErrorResponse},
        503: {
            "description": "Speech recognition model not available",
            "model": ErrorResponse,
        },
    },
)
def extract_lyrics(minio_path: str):
    """
    Extract lyrics (text) from an audio file using speech recognition.

    This endpoint uses the OpenAI Whisper model to transcribe audio to text.
    It returns the complete transcription as a single string.

    **How it works:**
    - Loads audio using librosa at 16kHz (Whisper requirement)
    - Processes audio through Whisper model
    - Returns plain text transcription

    **Supported formats:**
    - MP3, WAV, M4A, FLAC, OGG

    **Processing time:**
    - Depends on audio length (typically 2-3x real-time)

    Args:
        audio_file: Audio file to process (mp3, wav, m4a, etc.)

    Returns:
        JSON response containing extracted lyrics and metadata

    Raises:
        HTTPException: If file is invalid or processing fails
    """

    try:
        logger.info("Processing audio file...")
        minio_service = MinIOService(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
            bucket_name=settings.MINIO_BUCKET_NAME,
        )
        bytes_data = minio_service.get_file(minio_path)
        bytesIO = BytesIO(bytes_data)

        # Extract transcription with timestamps
        transcription: TranscriptionResult = extractor.extract(bytesIO)

        # Calculate duration from chunks
        duration_seconds = 0.0
        if transcription.chunks:
            duration_seconds = transcription.chunks[-1].end

        return LyricsExtractionResponse(
            text=transcription.text,
            duration_seconds=duration_seconds,
            sample_rate=16000,
        )

    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        raise HTTPException(status_code=500, detail="Error processing audio file")


@lyrics_router.post(
    "/with-timestamps",
    response_model=LyricsWithTimestampsResponse,
    summary="Extract lyrics with timestamps",
    description="Extract lyrics with timestamps from an audio file using chunked Whisper processing",
    responses={
        200: {
            "description": "Lyrics with timestamps extracted successfully",
            "model": LyricsWithTimestampsResponse,
        },
        400: {
            "description": "Invalid file type (not an audio file)",
            "model": ErrorResponse,
        },
        500: {"description": "Error processing audio file", "model": ErrorResponse},
        503: {
            "description": "Speech recognition model not available",
            "model": ErrorResponse,
        },
    },
)
async def extract_lyrics_with_timestamps(minio_path: str):
    """
    Extract lyrics with timestamps from an audio file.

    This endpoint processes audio to provide time-stamped lyrics with improved
    accuracy through forced alignment, useful for karaoke applications where
    timing is important.

    **How it works:**
    - Loads audio using librosa at 16kHz
    - Processes audio through Whisper speech recognition
    - Applies forced alignment to refine word-level timestamps
    - Returns lyrics with accurate start/end times for each word

    **Supported formats:**
    - MP3, WAV, M4A, FLAC, OGG

    **Processing time:**
    - Depends on audio length (typically 2-3x real-time)

    Args:
        minio_path: Path to the audio file in Minio storage

    Returns:
        JSON response containing timestamped lyrics and metadata

    Raises:
        HTTPException: If file is invalid or processing fails
    """

    try:
        logger.info("Processing audio file for timestamped lyrics...")
        minio_service = MinIOService(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
            bucket_name=settings.MINIO_BUCKET_NAME,
        )
        bytes_data = minio_service.get_file(minio_path)
        bytesIO = BytesIO(bytes_data)

        # Extract transcription with timestamps
        transcription: TranscriptionResult = extractor.extract(bytesIO)

        # Calculate duration from chunks
        duration_seconds = 0.0
        if transcription.chunks:
            duration_seconds = transcription.chunks[-1].end

        return LyricsWithTimestampsResponse(
            text=transcription.text,
            chunks=transcription.chunks,
            total_duration_seconds=duration_seconds,
            sample_rate=16000,
        )

    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        raise HTTPException(status_code=500, detail="Error processing audio file")
