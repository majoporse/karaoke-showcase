
import logging
from io import BytesIO
from typing import Any, Tuple

from librosa import load
from scipy.io import wavfile
from spleeter.separator import Separator

from config.model_config import CONFIG

from .base_model import BaseSeparator

logger = logging.getLogger(__name__)


class SpleeterSeparator(BaseSeparator):
    """Spleeter voice separation model."""

    def __init__(self):
        """Initialize Spleeter model."""
        super().__init__()
        spleeter_config = CONFIG.voice_separation.spleeter
        self.model = Separator(
            params_descriptor=spleeter_config.params_descriptor,
            MWF=spleeter_config.mwf,
            multiprocess=spleeter_config.multiprocess,
        )

    def separate_vocals(self, audio_file: BytesIO) -> Tuple[BytesIO, BytesIO]:
        try:
            waveform, samplerate = self._get_audio_ndarray(audio_file)

            if waveform.shape[0] < waveform.shape[1]:  # type: ignore
                waveform = waveform.T  # type: ignore

            prediction = self.model.separate(waveform)  # type: ignore

            vocals_file = BytesIO()
            accompaniment_file = BytesIO()

            wavfile.write(vocals_file, samplerate, prediction["vocals"])  # type: ignore
            wavfile.write(
                accompaniment_file,
                samplerate,
                prediction["accompaniment"],  # type: ignore
            )

            # Reset buffer positions so they can be read by the caller
            vocals_file.seek(0)
            accompaniment_file.seek(0)

            logger.info("Voice separation completed successfully")

            return vocals_file, accompaniment_file
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise

    def _get_audio_ndarray(self, audio_file: BytesIO) -> Tuple[Any, int]:
        """Convert audio file to numpy array."""
        audio_file.seek(0)
        audio_data, samplerate = load(audio_file, sr=None, mono=False)

        # Convert to numpy array with shape (channels, samples)
        if audio_data.ndim == 1:
            # Mono audio: reshape to (1, samples)
            audio_ndarray = audio_data.reshape(1, -1)
        else:
            # Stereo/multi-channel: (channels, samples)
            audio_ndarray = audio_data

        logger.info(
            f"Audio ndarray prepared: shape={audio_ndarray.shape}, samplerate={samplerate}"
        )

        return audio_ndarray, int(samplerate)
