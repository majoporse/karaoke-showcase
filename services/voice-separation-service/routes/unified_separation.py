import logging
import traceback

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from starlette.responses import StreamingResponse

from config import CONFIG
from models.common import ErrorResponse
from services.unified_separation_service import separate_vocals

logger = logging.getLogger(__name__)

# Initialize router with prefix and tags
unified_router = APIRouter(
    prefix="/separate-voice",
    tags=["Voice Separation"],
)


class SeparateVoiceResponse(BaseModel):
    vocals_path: str = Field(
        ..., description="Object storage path to the separated vocals file"
    )
    accompaniment_path: str = Field(
        ..., description="Object storage path to the separated accompaniment file"
    )


@unified_router.post(
    "",
    response_model=SeparateVoiceResponse,
    summary="Separate vocals from music",
    description="Accepts an audio file and returns a path to object storage for the separated vocals and accompaniment tracks using the configured model",
    responses={
        200: {
            "description": "Voice separation successful - returns ZIP file",
        },
        400: {
            "description": "Invalid file type (not an audio file)",
            "model": ErrorResponse,
        },
        500: {"description": "Error processing audio file", "model": ErrorResponse},
        503: {
            "description": "Voice separation service not ready",
            "model": ErrorResponse,
        },
    },
)
def separate_voice_unified(
    minio_path: str,
) -> SeparateVoiceResponse:
    logger.info(f"Received voice separation request for file: {minio_path}")

    try:
        vocals, accompaniment = separate_vocals(minio_path)

        return SeparateVoiceResponse(
            vocals_path=vocals, accompaniment_path=accompaniment
        )
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")


@unified_router.get(
    "/config",
    summary="Get voice separation configuration",
    description="Returns the current voice separation configuration including the active model",
    responses={
        200: {
            "description": "Configuration information",
        },
    },
)
async def get_configuration():
    try:

        active_model = CONFIG.voice_separation.active_model

        return {
            "active_model": active_model,
            "available_models": {
                "demucs": {
                    "description": "Facebook's Demucs model - highest quality separation",
                    "memory_efficient": False,
                    "quality": "high",
                    "supported_formats": ["mp3", "wav", "m4a", "flac", "ogg"],
                },
                "spleeter": {
                    "description": "Deezer's Spleeter model - fast and efficient separation",
                    "memory_efficient": True,
                    "quality": "medium",
                    "supported_formats": ["mp3", "wav", "m4a", "flac"],
                },
            },
        }

    except Exception as e:
        logger.error(f"Error getting configuration: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error getting configuration: {str(e)}"
        )
