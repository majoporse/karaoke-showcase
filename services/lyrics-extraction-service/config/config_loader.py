import json
from dataclasses import asdict
from pathlib import Path

import yaml

from config.config import Config


def load_config() -> Config:

    path = Path(__file__).parent / "config.yaml"
    print(f"Loading config from {path}")

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path) as f:
        if path.suffix == ".json":
            config_dict = json.load(f)
            print(f"Loaded config: {config_dict}")
        elif path.suffix in [".yaml", ".yml"]:
            config_dict = yaml.safe_load(f)
            print(f"Loaded config: {config_dict}")
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

    return Config(**config_dict)


def save_config(config: Config, path: str | Path = "config.json") -> None:
    """Save configuration to JSON or YAML file."""
    path = Path(path)
    config_dict = asdict(config)

    with open(path, "w") as f:
        if path.suffix == ".json":
            json.dump(config_dict, f, indent=2)
        elif path.suffix in [".yaml", ".yml"]:
            yaml.dump(config_dict, f, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
