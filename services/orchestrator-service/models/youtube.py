from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Extra


class YouTubeVideoMetadata(BaseModel):
    id: str
    title: str
    uploader: str
    uploader_url: str
    thumbnail: str
    thumbnail_url: str
    description: Optional[str] = None
    uploader_id: Optional[str] = None
    duration: Optional[float] = None  # seconds
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    dislike_count: Optional[int] = None
    upload_date: Optional[str] = None  # YYYYMMDD
    release_date: Optional[str] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    age_limit: Optional[int] = None
    is_live: Optional[bool] = None
    channel: Optional[str] = None
    channel_id: Optional[str] = None
    channel_url: Optional[str] = None
    duration_string: Optional[str] = None
    format_id: Optional[str] = None
    format_note: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    resolution: Optional[str] = None
    fps: Optional[float] = None
    vcodec: Optional[str] = None
    acodec: Optional[str] = None
    extent: Optional[str] = None
    format: Optional[str] = None

    model_config = ConfigDict(extra=Extra.allow)
