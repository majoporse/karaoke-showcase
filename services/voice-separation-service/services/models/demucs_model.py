"""
Demucs voice separation model implementation.
Uses Facebook's Demucs for high-quality voice separation.
"""

import logging
from io import BytesIO
from typing import Tuple

from demucs_infer.api import Separator
from librosa import load
from scipy.io import wavfile
from torch import from_numpy

from config.model_config import CONFIG

from .base_model import BaseSeparator

logger = logging.getLogger(__name__)


class DemucsSeparator(BaseSeparator):
    """Demucs voice separation model."""

    def __init__(self):
        """Initialize Demucs model."""
        super().__init__()
        demucs_config = CONFIG.voice_separation.demucs
        print(demucs_config)
        self.separator = Separator(
            device=demucs_config.device,
            model=demucs_config.model,
            split=demucs_config.split,
            progress=demucs_config.progress,
        )
        self.samplerate = self.separator.samplerate
        self._initialized = True

    def separate_vocals(self, audio_file: BytesIO) -> Tuple[BytesIO, BytesIO]:
        """Separate vocals using Demucs."""

        separator = self.separator
        samplerate = self.samplerate

        # Validate
        if separator is None:
            raise RuntimeError("Demucs separator not initialized")
        if samplerate is None:
            raise RuntimeError("Samplerate not set")

        try:
            audio_tensor, sr = self._get_audio_tensor(audio_file)

            logger.info("Separating audio using Demucs")
            result = separator.separate_tensor(audio_tensor, sr=int(sr))

            origin, separated = result[:2]
            vocals = separated["vocals"]
            accompaniment = origin - vocals

            vocals_file = BytesIO()
            accompaniment_file = BytesIO()

            vocals_data = vocals.cpu().numpy().T
            accompaniment_data = accompaniment.cpu().numpy().T

            wavfile.write(vocals_file, samplerate, vocals_data)
            wavfile.write(accompaniment_file, samplerate, accompaniment_data)

            logger.info("Voice separation completed successfully")

            return vocals_file, accompaniment_file
        except Exception as e:
            logger.error(f"Error processing audio with Demucs: {e}")
            raise

    def _get_audio_tensor(self, audio_file: BytesIO):
        """Convert audio file to torch tensor."""
        audio_file.seek(0)
        audio_data, samplerate = load(audio_file, sr=None, mono=False)

        # Convert to torch tensor with shape (channels, samples)
        if audio_data.ndim == 1:
            # Mono audio: reshape to (1, samples)
            audio_tensor = from_numpy(audio_data).unsqueeze(0).float()
        else:
            # Stereo/multi-channel: (channels, samples)
            audio_tensor = from_numpy(audio_data).float()

        logger.info(
            f"Audio tensor prepared: shape={audio_tensor.shape}, samplerate={samplerate}"
        )

        return audio_tensor, samplerate
