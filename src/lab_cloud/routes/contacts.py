"""Contacts API endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, status
from pymongo.database import Database

from lab_cloud.db import get_database
from lab_cloud.schemas import ContactIn, ContactOut

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("", response_model=ContactOut, status_code=status.HTTP_201_CREATED)
def create_contact(
    payload: ContactIn,
    db: Database[Any] = Depends(get_database),
) -> ContactOut:
    """Insert a new contact into the collection."""
    result = db["contacts"].insert_one(payload.model_dump())
    return ContactOut(id=str(result.inserted_id), **payload.model_dump())


@router.get("", response_model=list[ContactOut])
def list_contacts(
    db: Database[Any] = Depends(get_database),
) -> list[ContactOut]:
    """Return all contacts stored in the collection."""
    return [
        ContactOut(id=str(doc["_id"]), name=doc["name"], email=doc["email"])
        for doc in db["contacts"].find()
    ]