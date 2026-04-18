from dishka import Provider, Scope, make_async_container
from dotenv import load_dotenv

from config import Settings, settings
from services.lyrics_extraction_service import LyricsExtractionService
from services.minio_service import MinIOService
from services.orchestrator_service import ProcessingOrchestrator
from services.song_management_service import SongManagementService
from services.voice_separation_service import VoiceSeparationService
from services.youtube_downloader import YouTubeDownloader

load_dotenv()


# ============================================================================
# Settings Provider (APP scope)
# ============================================================================

settings_provider = Provider(scope=Scope.APP)
settings_provider.provide(lambda: settings, provides=Settings)


# ============================================================================
# Infrastructure Provider (APP scope)
# ============================================================================

infra_provider = Provider(scope=Scope.APP)


@infra_provider.provide
def get_minio_service() -> MinIOService:
    return MinIOService(
        endpoint=settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE,
        bucket_name=settings.MINIO_BUCKET_NAME,
        server_url=settings.SERVER_URL,
    )


# ============================================================================
# External API Services Provider (APP scope)
# ============================================================================

external_api_provider = Provider(scope=Scope.APP)

external_api_provider.provide(VoiceSeparationService)
external_api_provider.provide(LyricsExtractionService)
external_api_provider.provide(SongManagementService)


@external_api_provider.provide
def get_youtube_downloader(settings: Settings) -> YouTubeDownloader:
    """Initialize YouTubeDownloader with authentication from settings."""
    return YouTubeDownloader(
        cookies_path=settings.YOUTUBE_COOKIES_PATH
        if settings.YOUTUBE_COOKIES_PATH
        else None,
        po_token=settings.YOUTUBE_PO_TOKEN if settings.YOUTUBE_PO_TOKEN else None,
        pot_url=settings.POT_URL,
        proxy_url=settings.PROXY_URL
    )


# ============================================================================
# Orchestrator Provider (APP scope)
# ============================================================================

orchestrator_provider = Provider(scope=Scope.APP)
orchestrator_provider.provide(ProcessingOrchestrator)


# ============================================================================
# Export all providers as a tuple for container initialization
# ============================================================================

providers = (
    settings_provider,
    infra_provider,
    external_api_provider,
    orchestrator_provider,
)

container = make_async_container(*providers)
