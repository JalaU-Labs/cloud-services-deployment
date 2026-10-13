"""Pydantic schemas for the API."""

from pydantic import BaseModel, EmailStr, Field


class ContactIn(BaseModel):
    """Payload for creating a new contact."""

    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class ContactOut(ContactIn):
    """Representation of a stored contact."""

    id: str