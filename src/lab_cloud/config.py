"""Configuration loading from environment variables."""

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from the environment."""

    mongodb_uri: str
    mongodb_db: str
    app_env: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached application settings."""
    return Settings(
        mongodb_uri=os.getenv("MONGODB_URI", ""),
        mongodb_db=os.getenv("MONGODB_DB", "lab_cloud"),
        app_env=os.getenv("APP_ENV", "development"),
    )
