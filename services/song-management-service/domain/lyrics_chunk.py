from pydantic import BaseModel


class LyricsChunk(BaseModel):
    start: float = 0.0
    end: float = 0.0
    text: str = ""
