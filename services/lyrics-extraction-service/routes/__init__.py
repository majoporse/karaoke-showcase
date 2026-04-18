"""
Routes module for lyrics extraction service.

This module exports all API route routers for the lyrics extraction service.
"""

from .lyrics import lyrics_router
from .health import health_router

__all__ = [
    "lyrics_router",
    "health_router",
]
