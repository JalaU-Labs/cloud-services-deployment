"""Tests for the MongoDB client management module."""

import pytest

from lab_cloud import db as db_module


def test_get_database_raises_without_uri(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that a missing MONGODB_URI raises a clear error."""
    monkeypatch.setattr(
        db_module,
        "get_settings",
        lambda: type(
            "S",
            (),
            {"mongodb_uri": "", "mongodb_db": "test_db", "app_env": "test"},
        )(),
    )
    db_module._client.cache_clear()
    with pytest.raises(RuntimeError, match="MONGODB_URI is not configured"):
        db_module.get_database()
    db_module._client.cache_clear()
