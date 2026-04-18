from typing import List, Literal, Optional

from chanx.messages.base import BaseMessage
from pydantic import BaseModel, Field

from models.processing import Chunk
from models.youtube import YouTubeVideoMetadata


class ProcessingStartPayload(BaseModel):
    current_step: int = Field(
        default=0,
        description="Current step number",
        json_schema_extra={"example": 0},
    )
    total_steps: int = Field(
        default=5,
        description="Total number of steps",
        json_schema_extra={"example": 5},
    )
    desc: str = Field(
        ...,
        description="Status message",
        json_schema_extra={"example": "Initializing"},
    )
    youtube_url: str = Field(
        ...,
        description="YouTube URL to process",
        json_schema_extra={"example": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
    )


class ProcessingResult(BaseModel):
    success: Optional[bool] = Field(
        default=None,
        description="Whether processing was successful (only set on completion)",
        json_schema_extra={"example": True},
    )
    vocals_path: Optional[str] = Field(
        default=None,
        description="Download URL for extracted vocals track",
        json_schema_extra={"example": "/download/vocals.mp3"},
    )
    accompaniment_path: Optional[str] = Field(
        default=None,
        description="Download URL for accompaniment track",
        json_schema_extra={"example": "/download/accompaniment.mp3"},
    )
    lyrics: Optional[str] = Field(
        default=None,
        description="Full transcribed lyrics as plain text",
        json_schema_extra={
            "example": "Never gonna give you up\nNever gonna let you down"
        },
    )
    chunks: Optional[List[Chunk]] = Field(
        default=None,
        description="List of lyrics segments with timestamps",
    )
    yt_metadata: Optional[YouTubeVideoMetadata] = Field(
        default=None,
        description="YouTube video metadata",
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if processing failed",
        json_schema_extra={"example": "Invalid YouTube URL"},
    )


class ProcessingOutputPayload(BaseModel):
    current_step: int = Field(
        ...,
        description="Current step number (0-5)",
        json_schema_extra={"example": 2},
    )
    total_steps: int = Field(
        default=5,
        description="Total number of steps",
        json_schema_extra={"example": 5},
    )
    desc: str = Field(
        ...,
        description="Progress or status message",
        json_schema_extra={"example": "Downloading audio"},
    )
    result: Optional[ProcessingResult] = Field(
        default=None,
        description="Result information (only set on completion or error)",
    )


class ProcessingOutputMessage(BaseMessage):
    action: Literal["processing_output"] = "processing_output"
    payload: ProcessingOutputPayload


# class JobProgressSubscriptionPayload(BaseModel):
#     job_id: str = Field(
#         ...,
#         description="Unique identifier for the job to subscribe to",
#         json_schema_extra={"example": "job-123-abc-def"},
#     )

class JobProgressSubscriptionMessage(BaseMessage):
    action: Literal["job_progress_subscribe"] = "job_progress_subscribe"
    payload: None


