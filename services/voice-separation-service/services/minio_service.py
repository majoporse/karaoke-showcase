import io
import logging
from datetime import timedelta
from typing import Optional

from minio import Minio
from minio.error import S3Error

logger = logging.getLogger(__name__)


class MinIOService:
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        secure: bool = False,
        bucket_name: str = "karaoke",
    ):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = secure
        self.bucket_name = bucket_name

        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )

        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Created MinIO bucket: {self.bucket_name}")
            else:
                logger.debug(f"MinIO bucket already exists: {self.bucket_name}")
        except S3Error as e:
            logger.error(f"Failed to ensure bucket exists: {e}")
            raise

    def upload_file(
        self,
        file_data: bytes,
        object_name: str,
        bucket_name: Optional[str] = None,
        content_type: str = "application/octet-stream",
    ) -> str:
        bucket = bucket_name or self.bucket_name

        try:
            file_size = len(file_data)
            self.client.put_object(
                bucket,
                object_name,
                io.BytesIO(file_data),
                length=file_size,
                content_type=content_type,
            )
            logger.info(f"Uploaded {object_name} to bucket {bucket}")
            return object_name
        except S3Error as e:
            logger.error(f"Failed to upload {object_name}: {e}")
            raise

    def get_file(self, object_name: str, bucket_name: Optional[str] = None) -> bytes:
        bucket = bucket_name or self.bucket_name

        try:
            response = self.client.get_object(bucket, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            logger.info(f"Downloaded {object_name} from bucket {bucket}")
            return data
        except S3Error as e:
            logger.error(f"Failed to download {object_name}: {e}")
            raise

    def list_objects(
        self, prefix: str = "", bucket_name: Optional[str] = None
    ) -> list[str]:
        bucket = bucket_name or self.bucket_name

        try:
            objects = self.client.list_objects(bucket, prefix=prefix)
            object_list = [
                obj.object_name for obj in objects if obj.object_name is not None
            ]
            logger.info(f"Listed {len(object_list)} objects in bucket {bucket}")
            return object_list
        except S3Error as e:
            logger.error(f"Failed to list objects: {e}")
            raise

    def get_presigned_url(
        self,
        object_name: str,
        bucket_name: Optional[str] = None,
        expiration: int = 3600,
    ) -> str:
        bucket = bucket_name or self.bucket_name

        try:
            url = self.client.get_presigned_url(
                "GET", bucket, object_name, expires=timedelta(seconds=expiration)
            )
            logger.info(f"Generated presigned URL for {object_name}")
            return url
        except S3Error as e:
            logger.error(f"Failed to generate presigned URL for {object_name}: {e}")
            raise

    def remove_object(
        self,
        object_name: str,
        bucket_name: Optional[str] = None,
    ) -> None:
        bucket = bucket_name or self.bucket_name

        try:
            self.client.remove_object(bucket, object_name)
            logger.info(f"Removed object {object_name} from bucket {bucket}")
        except S3Error as e:
            logger.error(f"Failed to remove object {object_name}: {e}")
            raise
