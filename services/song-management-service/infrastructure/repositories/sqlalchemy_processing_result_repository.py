import logging
from typing import List, Optional
from uuid import UUID

from dishka.entities.depends_marker import FromDishka
from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.cache_key import STATIC_CACHE_KEY

from domain import Lyrics as DomainLyrics
from domain import LyricsChunk as DomainLyricsChunk
from domain import LyricsCreate as DomainLyricsCreate
from domain import ProcessingResult
from domain import ProcessingResult as DomainProcessingResult
from domain.files import get_accompaniment_path, get_vocal_path
from domain.processing_result import (
    ProcessingResultCreate as DomainProcessingResultCreate,
)
from domain.processing_result import (
    ProcessingResultUpdate as DomainProcessingResultUpdate,
)
from infrastructure.elasticsearch.client import get_elasticsearch_index
from infrastructure.models import ProcessingResult as SQLAlchemyProcessingResult
from services.repository_interfaces.processing_result_repository import (
    ProcessingResultRepository,
)

logger = logging.getLogger(__name__)


class SQLAlchemyProcessingResultRepository(ProcessingResultRepository):
    def __init__(
        self,
        db_session: FromDishka[AsyncSession],
        es_client: Elasticsearch,
    ):
        self.db = db_session
        self.es = es_client
        self.index_name = get_elasticsearch_index()

    async def get_by_id(self, result_id: UUID) -> Optional[DomainProcessingResult]:
        result = await self.db.execute(
            select(SQLAlchemyProcessingResult).filter(
                SQLAlchemyProcessingResult.id == result_id
            )
        )
        es_response = self.es.get(index=self.index_name, id=str(result_id))
        db_result = result.scalar_one_or_none()

        if not db_result or not es_response:
            return None

        return self._to_domain(db_result, es_response)

    async def search_by_query(
        self,
        query: str,
        language: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[List[DomainProcessingResult], int]:

        try:
            search_query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "multi_match": {
                                    "query": query,
                                    "fields": [
                                        "title",
                                        "uploader",
                                        "full_text",
                                    ],
                                    "type": "bool_prefix",
                                    "fuzziness": "AUTO",
                                    "zero_terms_query": "all",
                                    "minimum_should_match": "1",
                                }
                            }
                        ]
                    }
                },
                "sort": [
                    {"_score": {"order": "desc"}},
                    {"created_at": {"order": "desc"}},
                ],
            }

            if language:
                search_query["query"]["bool"]["filter"] = [
                    {"term": {"language": language}}
                ]

            response = self.es.search(
                index=self.index_name,
                body=search_query,
                size=limit,
                from_=offset,
                track_total_hits=True,
            )

            hits = response["hits"]["hits"]
            total_count = response["hits"]["total"]["value"]

            db_results = [
                await self.db.execute(
                    select(SQLAlchemyProcessingResult).filter(
                        SQLAlchemyProcessingResult.id == hit["_id"]
                    )
                )
                for hit in hits
            ]
            db_results = [db_result.scalar_one_or_none() for db_result in db_results]
            db_results = [db_result for db_result in db_results if db_result]

            res = [
                self._to_domain(db_result, hit)
                for hit, db_result in zip(hits, db_results)
            ]

            return res, total_count
        except Exception:
            return [], 0

    async def create(
        self, processing_result: DomainProcessingResultCreate
    ) -> DomainProcessingResult:
        db_result = self._to_sqlalchemy(processing_result)
        self.db.add(db_result)
        await self.db.commit()
        await self.db.refresh(db_result)

        lyrics_domain = processing_result.lyrics.to_lyrics(db_result.id)
        processing_result_domain = DomainProcessingResult(
            id=db_result.id,
            youtube_url=db_result.youtube_url,
            youtube_video_id=db_result.youtube_video_id,
            title=db_result.title,
            uploader=db_result.uploader,
            uploader_url=db_result.uploader_url,
            thumbnail_url=db_result.thumbnail_url,
            thumbnail=db_result.thumbnail,
            created_at=db_result.created_at,
            error_message=db_result.error_message,
            lyrics=lyrics_domain,
        )

        try:
            self.es.index(
                index=self.index_name,
                id=str(processing_result_domain.id),
                body=processing_result_domain.model_dump(),
            )
        except Exception as e:
            logger.error(f"Failed to index processing result: {e}")

        return processing_result_domain

    async def update(
        self, result_id: UUID, processing_result: DomainProcessingResultUpdate
    ) -> Optional[DomainProcessingResult]:

        result = await self.db.execute(
            select(SQLAlchemyProcessingResult).filter(
                SQLAlchemyProcessingResult.id == result_id
            )
        )
        db_result = result.scalar_one_or_none()
        if not db_result:
            return None

        for field, value in processing_result.model_dump(exclude_unset=True).items():
            setattr(db_result, field, value)

        await self.db.commit()
        await self.db.refresh(db_result)

        response = self.es.update(
            index=self.index_name,
            id=str(result_id),
            body={"doc": processing_result.model_dump(exclude={"id"})},
        )

        if response["result"] == "noop":
            return None

        return self._to_domain(db_result, response)

    async def delete(self, result_id: UUID) -> bool:
        result = await self.db.execute(
            select(SQLAlchemyProcessingResult).filter(
                SQLAlchemyProcessingResult.id == result_id
            )
        )
        db_result = result.scalar_one_or_none()
        if not db_result:
            return False

        await self.db.delete(db_result)
        await self.db.commit()
        response = self.es.delete(index=self.index_name, id=str(result_id))
        return response["result"] == "deleted"

    @staticmethod
    def get_source(document: ObjectApiResponse) -> dict:
        return document["_source"]

    def _to_domain(
        self, db_result: SQLAlchemyProcessingResult, es_result: ObjectApiResponse
    ) -> DomainProcessingResult:

        source = self.get_source(es_result)
        lyrics = source.get("lyrics", {})

        chunks = [
            DomainLyricsChunk(
                start=chunk.get("start", 0.0),
                end=chunk.get("end", 0.0),
                text=chunk.get("text", ""),
            )
            for chunk in lyrics.get("chunks", [])
        ]

        id = UUID(source["id"]) if "id" in source else None
        if id is None:
            raise ValueError("Lyrics document is missing ID")

        lyrics = DomainLyrics(
            processing_id=id,
            full_text=source.get("full_text", ""),
            chunks=chunks,
            language=source.get("language", "en"),
            confidence_score=source.get("confidence_score"),
        )

        return DomainProcessingResult(
            id=db_result.id,
            youtube_url=db_result.youtube_url,
            youtube_video_id=db_result.youtube_video_id,
            title=db_result.title,
            uploader=db_result.uploader,
            uploader_url=db_result.uploader_url,
            thumbnail_url=db_result.thumbnail_url,
            thumbnail=db_result.thumbnail,
            created_at=db_result.created_at,
            error_message=db_result.error_message,
            lyrics=lyrics,
        )

    @staticmethod
    def validate_es_result(db_result: SQLAlchemyProcessingResult, es_result: dict):
        # validate every field in db_result with es_result
        if not db_result:
            raise ValueError("Database result is None")
        if not es_result:
            raise ValueError("ES result is None")

        if es_result.get("processing_id") != db_result.id:
            logger.warning("Database result ID does not match ES result ID")
        if es_result.get("youtube_url") != db_result.youtube_url:
            logger.warning(
                "Database result youtube_url does not match ES result youtube_url"
            )
        if es_result.get("youtube_video_id") != db_result.youtube_video_id:
            logger.warning(
                "Database result youtube_video_id does not match ES result youtube_video_id"
            )
        if es_result.get("title") != db_result.title:
            logger.warning("Database result title does not match ES result title")
        if es_result.get("uploader") != db_result.uploader:
            logger.warning("Database result uploader does not match ES result uploader")
        if es_result.get("uploader_url") != db_result.uploader_url:
            logger.warning(
                "Database result uploader_url does not match ES result uploader_url"
            )
        if es_result.get("thumbnail_url") != db_result.thumbnail_url:
            logger.warning(
                "Database result thumbnail_url does not match ES result thumbnail_url"
            )
        if es_result.get("thumbnail") != db_result.thumbnail:
            logger.warning(
                "Database result thumbnail does not match ES result thumbnail"
            )
        if es_result.get("created_at") != db_result.created_at:
            logger.warning(
                "Database result created_at does not match ES result created_at"
            )
        if es_result.get("error_message") != db_result.error_message:
            logger.warning(
                "Database result error_message does not match ES result error_message"
            )

    def _to_sqlalchemy(
        self, result: DomainProcessingResultCreate
    ) -> SQLAlchemyProcessingResult:
        return SQLAlchemyProcessingResult(
            youtube_url=result.youtube_url,
            youtube_video_id=result.youtube_video_id,
            title=result.title,
            uploader=result.uploader,
            uploader_url=result.uploader_url,
            thumbnail_url=result.thumbnail_url,
            thumbnail=result.thumbnail,
            error_message=result.error_message,
        )
