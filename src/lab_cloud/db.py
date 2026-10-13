"""MongoDB client management."""

from functools import lru_cache
from typing import Any

from pymongo import MongoClient
from pymongo.database import Database

from lab_cloud.config import get_settings


@lru_cache(maxsize=1)
def _client() -> MongoClient[Any]:
    """Return a cached MongoDB client built from the environment."""
    settings = get_settings()
    if not settings.mongodb_uri:
        raise RuntimeError(
            "MONGODB_URI is not configured. Copy .env.example to .env and fill it in."
        )
    return MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=5000)


def get_database() -> Database[Any]:
    """FastAPI dependency that returns a MongoDB database handle."""
    return _client()[get_settings().mongodb_db]