import json
import logging
from pathlib import Path

from fastapi import APIRouter
from fastapi.applications import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
import yaml
    
logger = logging.getLogger(__name__)


def generate_openapi_spec(app: FastAPI) -> None:
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Try /app/ocr/ first (container), fallback to source dir
    output_path = Path("/app/ocr/openapi.json")
    if not output_path.parent.exists():
        output_path = Path(__file__).resolve().parent.parent / "openapi.json"
    output_path.write_text(json.dumps(schema, indent=2), encoding="utf-8")


def register_openapi_routes(app: FastAPI) -> None:
    router = APIRouter()

    @router.get("/docs", include_in_schema=False)
    async def swagger_ui():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url or "/openapi.json",
            title=f"{app.title} - Swagger UI",
        )
    
    
    @router.get("/openapi.yaml")
    async def get_openapi_yaml():
    
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        return JSONResponse(content=yaml.dump(openapi_schema), media_type="text/yaml")
    
    
    @router.get("/", include_in_schema=False)
    async def root():
    
        return {
            "name": app.title,
            "docs": "/docs",
            "openapi": "/openapi.json",
        }
        
    app.include_router(router)