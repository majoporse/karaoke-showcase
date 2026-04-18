import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import route routers
from config.settings import settings
from routes import health_router, unified_router
from routes.openapi import generate_openapi_spec, register_openapi_routes
from otel_setup import initialize_otel

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Initialize FastAPI application
app = FastAPI(
    title="Karaoke-Inator Voice Separation",
    description="AI-powered voice separation service that separates vocals from background music using advanced audio processing",
    version="1.0.0",
    contact={
        "name": "Karaoke-Inator API",
        "url": "https://github.com/majoporse/karaoke-inator",
    },
    openapi_tags=[
        {
            "name": "Voice Separation",
            "description": "Separate vocals from background music",
        },
        {
            "name": "Health",
            "description": "Service health monitoring",
        },
        {
            "name": "Utility",
            "description": "Basic service information",
        },
    ],
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


# Include all route routers first
app.include_router(unified_router)  # Unified endpoint
app.include_router(health_router)
register_openapi_routes(app)

# Initialize OpenTelemetry (after routes are registered)
logger.info("Initializing OpenTelemetry")
initialize_otel(app)


@app.on_event("startup")
async def startup_event():
    logger.info("startup: generating OpenAPI spec")
    generate_openapi_spec(app)
    logger.info("startup: OpenAPI spec written")


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.HOST, port=settings.PORT, log_level=settings.LOG_LEVEL
    )
