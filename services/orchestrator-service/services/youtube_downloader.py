import logging
import os
import traceback
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import yt_dlp
from fastapi import HTTPException

from models.youtube import YouTubeVideoMetadata

logger = logging.getLogger(__name__)


class YouTubeDownloader:
    def __init__(
        self,
        cookies_path: str | None = None,
        po_token: str | None = None,
        pot_url: str | None = None,
        proxy_url: str | None = None,
    ):
        """
        Initialize YouTubeDownloader with optional cookies and PO Token.

        Args:
            cookies_path: Path to YouTube cookies file (from private/incognito session)
            po_token: PO Token for bypassing YouTube's latest restrictions.
                     See: https://github.com/yt-dlp/yt-dlp/wiki/Extractors#po-token-guide
        """
        self.cookies_path = cookies_path
        self.po_token = po_token
        self.pot_url = pot_url
        self.proxy_url = proxy_url
        self.default_opts = self._build_options()
        

    def _build_options(self):

        logger.info(f"Building yt-dlp options with pot_url: {self.pot_url}")
        opts = {
            "socket_timeout": 30,
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            },
            "retries": 5,
            "fragment_retries": 5,
            "skip_unavailable_fragments": True,
            "extractor_args": {
                "youtubepot-bgutilhttp": {
                    "base_url": [self.pot_url],
                },
                "youtube": {
                    "player_client": ["android", "web", "ios"],
                    "player_skip_js_cache": True,
                },

            },
            # Bot evasion options
            "quiet": False,
            "no_warnings": False,
            "sleep_interval": 1,
        }
        
        if self.proxy_url:
            logger.info(f"Using proxy: {self.proxy_url}")
            opts["proxy"] = self.proxy_url

        # Add cookies if available (use from private/incognito session only)
        if self.cookies_path and os.path.exists(self.cookies_path):
            opts["cookiefile"] = self.cookies_path  # type: ignore
            logger.info(f"Using cookies from: {self.cookies_path}")

        return opts

    @staticmethod
    def clean_youtube_url(youtube_url: str) -> str:
        try:
            parsed = urlparse(youtube_url)
            query_params = parse_qs(parsed.query)

            video_id = None

            # Handle youtube.com URLs with 'v' parameter
            if "v" in query_params:
                video_id = query_params["v"][0]

            # Handle youtu.be short URLs (video ID is in the path)
            elif "youtu.be" in parsed.netloc:
                # Extract video ID from path (format: /VIDEO_ID)
                path_segments = parsed.path.strip("/").split("/")
                if path_segments and path_segments[0]:
                    video_id = path_segments[0]

            if not video_id:
                raise ValueError(f"No video ID found in URL: {youtube_url}")

            # Reconstruct URL with only the watch parameter
            cleaned_url = f"https://www.youtube.com/watch?v={video_id}"
            logger.info(f"Cleaned YouTube URL: {cleaned_url}")

            return cleaned_url
        except Exception as e:
            logger.error(f"Failed to clean YouTube URL: {str(e)}")
            raise ValueError(f"Invalid YouTube URL: {str(e)}")

    async def download_audio(self, youtube_url: str) -> bytes:
        logger.info(f"Starting YouTube download for URL: {youtube_url}")

        try:
            youtube_url = self.clean_youtube_url(youtube_url)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        import shutil
        import tempfile

        temp_dir = tempfile.mkdtemp()
        temp_path = Path(temp_dir)

        ydl_opts = {
            **self.default_opts,
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": str(temp_path / "%(title)s.%(ext)s"),
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
                info = ydl.extract_info(youtube_url, download=False)

                if "title" not in info or info["title"] is None:
                    raise ValueError("Video title is missing")

                ydl.download([youtube_url])

                # Find the actual downloaded MP3 file
                # yt_dlp sanitizes filenames, so we need to search for the file
                mp3_files = list(temp_path.glob("*.mp3"))
                logger.info(f"Files in temp_path: {list(temp_path.glob('*'))}")

                if not mp3_files:
                    raise FileNotFoundError(f"No MP3 file found in {temp_path}")

                if len(mp3_files) > 1:
                    logger.warning(
                        f"Multiple MP3 files found, using the most recently modified: {mp3_files}"
                    )
                    audio_file = max(mp3_files, key=lambda p: p.stat().st_mtime)
                else:
                    audio_file = mp3_files[0]

                logger.info(f"Audio downloaded successfully: {audio_file}")

                with open(audio_file, "rb") as f:
                    audio_bytes: bytes = f.read()
                logger.info(f"Audio file size: {len(audio_bytes)} bytes")

                return audio_bytes

        except Exception as e:
            logger.error(f"YouTube download failed: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"YouTube download failed: {str(e)}"
            )
        finally:
            shutil.rmtree(temp_path, ignore_errors=True)

    async def get_metadata(self, youtube_url: str) -> YouTubeVideoMetadata:
        logger.info(f"Fetching metadata for YouTube URL: {youtube_url}")

        try:
            url = self.clean_youtube_url(youtube_url)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        try:
            with yt_dlp.YoutubeDL(self.default_opts) as ydl:  # type: ignore
                info: yt_dlp.extractor.common._InfoDict = ydl.extract_info(
                    url, download=False
                )

                # Check required fields
                required_fields = [
                    "id",
                    "title",
                    "uploader",
                    "uploader_url",
                    "thumbnail",
                ]
                missing_fields = [
                    field
                    for field in required_fields
                    if field not in info or info[field] is None
                ]
                if missing_fields:
                    raise ValueError(
                        f"Missing required metadata fields: {', '.join(missing_fields)}"
                    )

                metadata = YouTubeVideoMetadata(
                    id=info["id"],
                    title=info.get("title") or "",
                    uploader=info.get("uploader") or "",
                    uploader_url=info.get("uploader_url") or "",
                    thumbnail=info.get("thumbnail") or "",
                    thumbnail_url=info.get("thumbnail_url") or "",
                    description=info.get("description"),
                    uploader_id=info.get("uploader_id"),
                    duration=info.get("duration"),
                    view_count=info.get("view_count"),
                    like_count=info.get("like_count"),
                    dislike_count=info.get("dislike_count"),
                    upload_date=info.get("upload_date"),
                    release_date=info.get("release_date"),
                    categories=info.get("categories"),
                    tags=info.get("tags"),
                    age_limit=info.get("age_limit"),
                    is_live=info.get("is_live"),
                    channel=info.get("channel"),
                    channel_id=info.get("channel_id"),
                    channel_url=info.get("channel_url"),
                    duration_string=info.get("duration_string"),
                    format_id=info.get("format_id"),
                    format_note=info.get("format_note"),
                    width=info.get("width"),
                    height=info.get("height"),
                    resolution=info.get("resolution"),
                    fps=info.get("fps"),
                    vcodec=info.get("vcodec"),
                    acodec=info.get("acodec"),
                    extent=info.get("extent"),
                    format=info.get("format"),
                )
                return metadata
        except Exception as e:
            logger.error(f"YouTube metadata extraction failed: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500, detail=f"YouTube metadata extraction failed: {str(e)}"
            )
