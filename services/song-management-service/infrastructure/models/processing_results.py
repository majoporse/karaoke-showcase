from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ProcessingResult(Base):
    __tablename__ = "processing_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    youtube_url: Mapped[str] = mapped_column(String(500))
    youtube_video_id: Mapped[str] = mapped_column(String(20))
    title: Mapped[str] = mapped_column(String(500))
    uploader: Mapped[str] = mapped_column(String(255))
    uploader_url: Mapped[str] = mapped_column(String(500))
    thumbnail_url: Mapped[str] = mapped_column(String(500))
    thumbnail: Mapped[str] = mapped_column(String(500))

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(String, nullable=True)
