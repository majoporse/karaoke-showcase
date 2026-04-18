from __future__ import annotations

import logging
from typing import List, Optional
from uuid import UUID

from domain import Lyrics, LyricsCreate, ProcessingResult
from domain.files import (
    ACCOMPANIMENT_FILE_NAME,
    VOCAL_FILE_NAME,
    get_path,
    get_vocal_path,
)
from domain.processing_result import ProcessingResultCreate, ProcessingResultUpdate
from services.minio_service import MinIOService
from services.repository_interfaces.processing_result_repository import (
    ProcessingResultRepository,
)

logger = logging.getLogger(__name__)


class ProcessingResultService:
    def __init__(
        self,
        processing_result_repository: ProcessingResultRepository,
        minio_service: MinIOService,
    ):
        self.processing_result_repository = processing_result_repository
        self.minio_service = minio_service

    async def get_result(self, result_id: UUID) -> Optional[ProcessingResult]:
        result = await self.processing_result_repository.get_by_id(result_id)

        if not result:
            return None

        return result

    async def create_result(
        self,
        processing_result_create: ProcessingResultCreate,
    ) -> ProcessingResult:

        created = await self.processing_result_repository.create(
            processing_result_create
        )

        if processing_result_create.vocals_minio_path:
            vocal_bytes = self.minio_service.get_file(
                processing_result_create.vocals_minio_path
            )
            object_name = get_path(created.id, VOCAL_FILE_NAME)
            vocal_path = self.minio_service.upload_file(vocal_bytes, object_name)
            logger.info(f"Uploaded vocal file for {created.id}")
            if not vocal_path:
                raise ValueError("Failed to upload vocal file")

        if processing_result_create.accompaniment_minio_path:
            accompaniment_bytes = self.minio_service.get_file(
                processing_result_create.accompaniment_minio_path
            )
            object_name = get_path(created.id, ACCOMPANIMENT_FILE_NAME)
            accompaniment_path = self.minio_service.upload_file(
                accompaniment_bytes, object_name
            )
            logger.info(f"Uploaded accompaniment file for {created.id}")
            if not accompaniment_path:
                raise ValueError("Failed to upload accompaniment file")

        return created

    async def update_result(
        self, result_id: UUID, processing_result: ProcessingResultUpdate
    ) -> Optional[ProcessingResult]:
        existing = await self.processing_result_repository.get_by_id(result_id)

        if not existing:
            return None

        updated = await self.processing_result_repository.update(
            result_id, processing_result
        )

        return updated

    async def delete_result(self, result_id: UUID) -> bool:
        # Get the result to check for associated lyrics
        result = await self.processing_result_repository.get_by_id(result_id)
        if not result:
            return False

        success = await self.processing_result_repository.delete(result_id)
        return success

    async def search_by_query(
        self,
        query: str,
        language: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[List[ProcessingResult], int]:
        
        results, total = await self.processing_result_repository.search_by_query(
            query, language, limit, offset
        )

        return results, total
