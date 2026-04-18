import io
import logging
from datetime import timedelta
from typing import Optional

from minio import Minio
from minio.error import S3Error

logger = logging.getLogger(__name__)


class MinIOService:
    """Service for interacting with MinIO object storage."""

    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        secure: bool = False,
        bucket_name: str = "karaoke",
    ):
        """
        Initialize MinIO service client.

        Args:
            endpoint: MinIO server endpoint (e.g., 'localhost:9000')
            access_key: MinIO access key
            secret_key: MinIO secret key
            secure: Use HTTPS for connection (default: False)
            bucket_name: Default bucket name for uploads
        """
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

        # Ensure bucket exists
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist."""
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
        """
        Upload a file to MinIO.

        Args:
            file_data: File content as bytes
            object_name: Name of the object in MinIO (path/filename)
            bucket_name: Override default bucket name (optional)
            content_type: MIME type of the file

        Returns:
            Object name (path) where file was uploaded

        Raises:
            S3Error: If upload fails
        """
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

    def upload_directory(
        self,
        files_dict: dict,
        prefix: str = "",
        bucket_name: Optional[str] = None,
    ) -> dict:
        """
        Upload multiple files to MinIO.

        Args:
            files_dict: Dictionary where keys are filenames and values are bytes
            prefix: Prefix to add to all object names (for organizing files)
            bucket_name: Override default bucket name (optional)

        Returns:
            Dictionary mapping original filenames to uploaded object names

        Raises:
            S3Error: If any upload fails
        """
        bucket = bucket_name or self.bucket_name
        uploaded = {}

        for filename, file_content in files_dict.items():
            if prefix:
                object_name = f"{prefix}/{filename}"
            else:
                object_name = filename

            try:
                self.upload_file(
                    file_content,
                    object_name,
                    bucket_name=bucket,
                )
                uploaded[filename] = object_name
            except S3Error as e:
                logger.error(f"Failed to upload {filename}: {e}")
                raise

        return uploaded

    def get_file(self, object_name: str, bucket_name: Optional[str] = None) -> bytes:
        """
        Download a file from MinIO.

        Args:
            object_name: Name of the object in MinIO
            bucket_name: Override default bucket name (optional)

        Returns:
            File content as bytes

        Raises:
            S3Error: If download fails
        """
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

    def list_objects(self, prefix: str = "", bucket_name: Optional[str] = None) -> list:
        """
        List objects in MinIO bucket.

        Args:
            prefix: Prefix to filter objects (optional)
            bucket_name: Override default bucket name (optional)

        Returns:
            List of object names

        Raises:
            S3Error: If listing fails
        """
        bucket = bucket_name or self.bucket_name

        try:
            objects = self.client.list_objects(bucket, prefix=prefix)
            object_list = [obj.object_name for obj in objects]
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
        """
        Generate a presigned URL for downloading a file from MinIO.

        Args:
            object_name: Name of the object in MinIO
            bucket_name: Override default bucket name (optional)
            expiration: URL expiration time in seconds (default: 1 hour)

        Returns:
            Presigned URL that can be used to download the file

        Raises:
            S3Error: If URL generation fails
        """
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
