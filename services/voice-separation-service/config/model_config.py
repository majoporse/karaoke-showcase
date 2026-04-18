from pathlib import Path

from pydantic import BaseModel
from yaml import dump, safe_load


class DemucsConfig(BaseModel):

    device: str = "cpu"
    split: bool = False
    channels: int = 2
    model: str = "htdemucs"
    progress: bool = False


class SpleeterConfig(BaseModel):

    params_descriptor: str = "spleeter:2stems"
    mwf: bool = False
    multiprocess: bool = False


class ServiceConfig(BaseModel):

    active_model: str
    demucs: DemucsConfig
    spleeter: SpleeterConfig = SpleeterConfig()


class VoiceSeparationConfig(BaseModel):

    voice_separation: ServiceConfig


def load_config() -> VoiceSeparationConfig:
    config_path = Path(__file__).parent / "voice_separation_config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        config_dict = safe_load(f)

    return VoiceSeparationConfig(**config_dict)


def save_config(config: VoiceSeparationConfig, path: str | Path | None = None) -> None:
    if path is None:
        path = Path(__file__).parent / "voice_separation_config.yaml"

    path = Path(path)
    config_dict = config.model_dump()

    with open(path, "w") as f:
        dump(config_dict, f, default_flow_style=False)


CONFIG = load_config()
