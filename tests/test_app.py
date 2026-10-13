"""Tests for the FastAPI application."""

from collections.abc import Iterator

import mongomock
import pytest
from fastapi.testclient import TestClient

from lab_cloud import __version__
from lab_cloud.app import app
from lab_cloud.db import get_database

_mock_client = mongomock.MongoClient()
_mock_db = _mock_client["test_db"]


def _override_get_database() -> mongomock.database.Database:
    return _mock_db


app.dependency_overrides[get_database] = _override_get_database

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clean_collection() -> Iterator[None]:
    """Ensure the contacts collection is empty before each test."""
    _mock_db["contacts"].delete_many({})
    yield
    _mock_db["contacts"].delete_many({})


def test_health_check() -> None:
    """Test that the health check endpoint returns the expected payload."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": __version__}


def test_create_contact() -> None:
    """Test creating a contact returns 201 and the stored payload."""
    response = client.post(
        "/contacts",
        json={"name": "Alice", "email": "alice@example.com"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Alice"
    assert body["email"] == "alice@example.com"
    assert isinstance(body["id"], str)
    assert body["id"]


def test_list_contacts_returns_stored_items() -> None:
    """Test listing contacts returns all stored items."""
    client.post("/contacts", json={"name": "Bob", "email": "bob@example.com"})
    client.post("/contacts", json={"name": "Carol", "email": "carol@example.com"})

    response = client.get("/contacts")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    names = {item["name"] for item in body}
    assert names == {"Bob", "Carol"}


def test_create_contact_rejects_invalid_payload() -> None:
    """Test validation rejects empty names and malformed emails."""
    response = client.post(
        "/contacts",
        json={"name": "", "email": "not-an-email"},
    )
    assert response.status_code == 422