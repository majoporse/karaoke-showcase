import logging
from contextlib import asynccontextmanager

import uvicorn
from chanx.fast_channels import asyncapi_docs, asyncapi_spec_json
from chanx.fast_channels.type_defs import AsyncAPIConfig
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from routes.job_progress_consumer import JobProgressConsumer
from config import settings
from di import container
from routes import health_router, processing_router, storage_router
from routes.openapi import generate_openapi_spec, register_openapi_routes
from otel_setup import initialize_otel

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Orchestrator Service...")

    # Initialize OpenTelemetry

    # Generate OpenAPI spec on startup
    logger.info("Generating OpenAPI spec...")
    try:
        generate_openapi_spec(app)
        logger.info("OpenAPI spec generated successfully")
    except Exception as e:
        logger.warning(f"Could not generate OpenAPI spec: {e}")

    yield

    # Shutdown
    logger.info("Shutting down Orchestrator Service...")


# Initialize FastAPI application
app = FastAPI(
    title="Karaoke-Inator Orchestrator",
    description="Master orchestration service for YouTube audio processing: voice separation and lyrics extraction",
    version="1.0.0",
    contact={
        "name": "Karaoke-Inator API",
        "url": "https://github.com/majoporse/karaoke-inator",
    },
    openapi_tags=[
        {
            "name": "Processing",
            "description": "Main audio processing operations",
        },
        {
            "name": "Health",
            "description": "Service health monitoring",
        },
        {
            "name": "Downloads",
            "description": "Download processed files",
        },
        {
            "name": "Utility",
            "description": "Basic service information",
        },
    ],
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Dishka container
setup_dishka(container=container, app=app)

# Include all route routers
app.include_router(processing_router)
app.include_router(health_router)
app.include_router(storage_router)
register_openapi_routes(app)


# Add WebSocket route for job progress streaming with job_id parameter
app.add_websocket_route("/ws/job-progress/{job_id}", JobProgressConsumer.as_asgi())


config = AsyncAPIConfig(
    title="Karaoke-Inator WebSocket API",
    description="Real-time WebSocket API for audio processing with progress updates",
    version="1.0.0",
)


@app.get("/asyncapi", response_class=HTMLResponse)
async def asyncapi_documentation(request: Request):
    return await asyncapi_docs(request=request, app=app, config=config)


@app.get("/asyncapi.json", response_class=JSONResponse)
async def asyncapi_specification(request: Request):
    return await asyncapi_spec_json(request=request, app=app, config=config)


initialize_otel(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        reload=True,
    )
