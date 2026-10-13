"""Tests for the FastAPI application."""

from fastapi.testclient import TestClient

from lab_cloud import __version__
from lab_cloud.app import app

client = TestClient(app)


def test_health_check() -> None:
    """Test that the health check endpoint returns the expected payload."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": __version__}
