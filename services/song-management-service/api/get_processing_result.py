from uuid import UUID
from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from services.processing_result_service import ProcessingResultService
from .common import ProcessingResultResponse


router = APIRouter(
    prefix="/processing-results", tags=["Processing Results"], route_class=DishkaRoute
)


@router.get("/{result_id}", response_model=ProcessingResultResponse)
async def get_result(result_id: UUID, service: FromDishka[ProcessingResultService]):
    result = await service.get_result(result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Processing result not found")
    return ProcessingResultResponse.from_domain(result)
