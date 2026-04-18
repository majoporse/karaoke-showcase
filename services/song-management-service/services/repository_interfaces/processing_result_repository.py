from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain import Lyrics, ProcessingResult
from domain.processing_result import ProcessingResultCreate, ProcessingResultUpdate


class ProcessingResultRepository(ABC):
    @abstractmethod
    async def get_by_id(self, result_id: UUID) -> Optional[ProcessingResult]:
        pass

    @abstractmethod
    async def create(
        self, processing_result: ProcessingResultCreate
    ) -> ProcessingResult:
        pass

    @abstractmethod
    async def update(
        self, result_id: UUID, processing_result: ProcessingResultUpdate
    ) -> Optional[ProcessingResult]:
        pass

    @abstractmethod
    async def delete(self, result_id: UUID) -> bool:
        pass

    @abstractmethod
    async def search_by_query(
        self,
        query: str,
        language: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[ProcessingResult], int]:
        pass
