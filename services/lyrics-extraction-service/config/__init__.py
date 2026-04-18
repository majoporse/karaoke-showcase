"""Configuration management for lyrics extraction service."""

from config.config import Config
from config.config_loader import load_config, save_config

__all__ = ["Config", "load_config", "save_config"]
