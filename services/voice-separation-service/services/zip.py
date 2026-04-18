import logging
import zipfile
from io import BytesIO

logger = logging.getLogger(__name__)


def write_zip(vocals_file: BytesIO, accompaniment_file: BytesIO) -> BytesIO:
    vocals_file.seek(0)
    accompaniment_file.seek(0)

    logger.info("Creating ZIP file in memory")
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        zipf.writestr("vocals.mp3", vocals_file.getvalue())
        zipf.writestr("accompaniment.mp3", accompaniment_file.getvalue())

    zip_content = zip_buffer.getvalue()

    logger.info(
        f"Voice separation completed successfully, ZIP size: {len(zip_content)} bytes"
    )

    return BytesIO(zip_content)
