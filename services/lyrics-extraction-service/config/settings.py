import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", "karaoke")

    PORT: int = int(os.getenv("PORT", "8002"))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    print("minio endpoint:", MINIO_ENDPOINT)


settings = Settings()
