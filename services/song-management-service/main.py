import logging
import os
from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine

from api.create_processing_result import router as create_router
from api.delete_processing_result import router as delete_router
from api.get_processing_result import router as get_router
from api.health import health_router
from api.openapi import generate_openapi_spec, register_openapi_routes
from api.search_processing_results_by_lyrics import router as search_router
from api.update_processing_result import router as update_router
from di import providers
from infrastructure.elasticsearch.client import init_elasticsearch
from infrastructure.models.base import Base
from setup_db import create_database_if_not_exists
from otel_setup import initialize_otel

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


create_database_if_not_exists()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Song Management Service...")

    # Initialize database

    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")

    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")

    # Initialize Elasticsearch
    try:
        init_elasticsearch()
        logger.info("Elasticsearch client initialized")
    except Exception as e:
        logger.warning(f"Could not initialize Elasticsearch: {e}")

    # Generate OpenAPI spec on startup
    logger.info("Generating OpenAPI spec...")
    try:
        generate_openapi_spec(app)
        logger.info("OpenAPI spec generated successfully")
    except Exception as e:
        logger.warning(f"Could not generate OpenAPI spec: {e}")

    yield

    # Shutdown
    logger.info("Shutting down Song Management Service...")


# Initialize FastAPI application
app = FastAPI(
    title="Song Management Service",
    description="CRUD API for managing songs, versions, processing results, and lyrics",
    version="1.0.0",
    contact={
        "name": "Karaoke-Inator API",
        "url": "https://github.com/majoporse/karaoke-inator",
    },
    openapi_tags=[
        {
            "name": "Processing Results",
            "description": "Processing result management endpoints",
        },
        {
            "name": "Health",
            "description": "Service health monitoring",
        },
    ],
    lifespan=lifespan,
    docs_url=None,  # Custom endpoint
    redoc_url=None,  # Custom endpoint
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


container = make_async_container(*providers)
setup_dishka(container=container, app=app)

app.include_router(get_router)
app.include_router(create_router)
app.include_router(update_router)
app.include_router(delete_router)
app.include_router(search_router)
app.include_router(health_router)
register_openapi_routes(app)

# Initialize OpenTelemetry (after routes are registered)
logger.info("Initializing OpenTelemetry")
initialize_otel(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)
