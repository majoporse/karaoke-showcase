from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from pydantic import BaseModel

from services.processing_result_service import ProcessingResultService
from .common import LyricsResponse, ProcessingResultResponse, PaginatedResponse

router = APIRouter(
    prefix="/processing-results", tags=["Processing Results"], route_class=DishkaRoute
)


@router.get("/", response_model=PaginatedResponse[ProcessingResultResponse])
async def search_processing_results(
    service: FromDishka[ProcessingResultService],
    q: str = Query(..., alias="query", description="Search query for lyrics content"),
    language: Optional[str] = Query(None, description="Filter by language"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(20, ge=1, le=100, description="Number of results per page"),
):
    offset = (page - 1) * limit
    results, total = await service.search_by_query(q, language, limit, offset)

    response_items = [
        ProcessingResultResponse.from_domain_with_lyrics(result) for result in results
    ]

    return PaginatedResponse.create(
        items=response_items,
        total=total,
        page=page,
        limit=limit,
    )
