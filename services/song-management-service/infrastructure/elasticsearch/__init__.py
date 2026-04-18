"""Elasticsearch module."""

from .client import get_es_client, init_elasticsearch
from .models import LyricsDocument

__all__ = ["get_es_client", "init_elasticsearch", "LyricsDocument"]
