import os
from typing import AsyncGenerator

from dishka import Provider, Scope
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from infrastructure.elasticsearch.client import get_es_client
from infrastructure.repositories.sqlalchemy_processing_result_repository import (
    SQLAlchemyProcessingResultRepository,
)
from services.minio_service import MinIOService
from services.processing_result_service import ProcessingResultService
from services.repository_interfaces.processing_result_repository import (
    ProcessingResultRepository,
)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
# ============================================================================
# Database Provider (REQUEST scope - new session per request)
# ============================================================================

db_provider = Provider(scope=Scope.REQUEST)


@db_provider.provide
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# ============================================================================
# Infrastructure Provider (APP scope - singleton)
# ============================================================================

infra_provider = Provider(scope=Scope.APP)


@infra_provider.provide
def get_elasticsearch_client() -> Elasticsearch:
    return get_es_client()


@infra_provider.provide
def get_minio_service() -> MinIOService:
    """Provide MinIO service client."""
    minio_endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    minio_access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    minio_secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    minio_secure = os.getenv("MINIO_SECURE", "False").lower() == "true"
    minio_bucket_name = os.getenv("MINIO_BUCKET_NAME", "karaoke")

    return MinIOService(
        endpoint=minio_endpoint,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=minio_secure,
        bucket_name=minio_bucket_name,
    )


# ============================================================================
# Repository Provider (REQUEST scope - depends on DB session)
# ============================================================================

repo_provider = Provider(scope=Scope.REQUEST)

repo_provider.provide(
    SQLAlchemyProcessingResultRepository, provides=ProcessingResultRepository
)


# ============================================================================
# Service Provider (REQUEST scope - depends on repositories)
# ============================================================================

service_provider = Provider(scope=Scope.REQUEST)

service_provider.provide(ProcessingResultService)


# ============================================================================
# Export all providers as a tuple for container initialization
# ============================================================================

providers = (
    db_provider,
    infra_provider,
    repo_provider,
    service_provider,
)
