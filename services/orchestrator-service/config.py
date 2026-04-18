import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Service URLs
    VOICE_SEPARATION_URL: str = os.getenv(
        "VOICE_SEPARATION_URL", "http://localhost:8001"
    )
    LYRICS_EXTRACTION_URL: str = os.getenv(
        "LYRICS_EXTRACTION_URL", "http://localhost:8002"
    )
    SONG_MANAGEMENT_URL: str = os.getenv("SONG_MANAGEMENT_URL", "http://localhost:8003")

    # MinIO Configuration
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", "karaoke")

    # Server Configuration
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

    # Redis Configuration (for RQ)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # YouTube Authentication
    # PO Token for YouTube downloads (see: https://github.com/yt-dlp/yt-dlp/wiki/Extractors#po-token-guide)
    YOUTUBE_PO_TOKEN: str = os.getenv("YOUTUBE_PO_TOKEN", "")
    # Path to cookies file exported from private/incognito YouTube session
    YOUTUBE_COOKIES_PATH: str = os.getenv("YOUTUBE_COOKIES_PATH", "")
    POT_URL: str = os.getenv("POT_URL", "")
    PROXY_URL: str = os.getenv("PROXY_URL", "")
    SERVER_URL: str = os.getenv("SERVER_URL", "")

    print("minio endpoint:", MINIO_ENDPOINT)


# Create global settings instance
settings = Settings()
