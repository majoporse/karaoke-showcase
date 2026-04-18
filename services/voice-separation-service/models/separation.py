"""
Voice Separation Service Models.

These models define the API contracts for the voice separation service,
including file uploads and separation results.
"""

from typing import Optional

from pydantic import BaseModel, Field


class VoiceSeparationRequest(BaseModel):
    """
    Request model for voice separation.

    Note: This is a placeholder since file uploads use UploadFile directly.
    For OpenAPI documentation purposes, this shows the expected parameters.
    """

    audio_file: Optional[str] = Field(
        default=None,
        description="Audio file to process (mp3, wav, m4a, etc.)",
        json_schema_extra={"example": "song.mp3"},
    )

