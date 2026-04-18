"""
Minimal configuration for lyrics extraction service.
"""

from dataclasses import dataclass


@dataclass
class Config:
    """Configuration for lyrics extraction."""

    # Faster Whisper parameters
    model_size: str = "large-v3"
    compute_type: str = "int8"
    device: str = "cuda"
    
    # Model parameters
    log_progress: bool = False
    word_timestamps: bool = True
    temperature: float = 0.0
    verbose: bool = False
    vad: bool = False
    vad_threshold: float = 0.5

    # Audio chunking
    chunk_duration: float = 30.0
    overlap_duration: float = 1.0

    # Pause-based chunking
    pause_threshold: float = 0.5  # Pause duration (seconds) to create new chunk

    # Initial prompt for transcription context
    initial_prompt: str | None = None
