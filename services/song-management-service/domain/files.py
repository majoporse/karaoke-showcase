from uuid import UUID

VOCAL_FILE_NAME = "vocal.mp3"
ACCOMPANIMENT_FILE_NAME = "accompaniment.mp3"


def get_path(lyrics_id: UUID, file_name: str) -> str:
    return f"lyrics/{lyrics_id}/{file_name}"


def get_vocal_path(lyrics_id: UUID) -> str:
    return get_path(lyrics_id, VOCAL_FILE_NAME)


def get_accompaniment_path(lyrics_id: UUID) -> str:
    return get_path(lyrics_id, ACCOMPANIMENT_FILE_NAME)
