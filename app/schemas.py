"""Pydantic v2 schemas for the notes API.

Only Pydantic v2 APIs are used here: ``model_config`` and ``field_validator``.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

TITEL_MAX_LENGTH = 100
TAGS_MAX_COUNT = 5


class NoteCreate(BaseModel):
    """Payload accepted by ``POST /notes``."""

    model_config = ConfigDict(extra="ignore")

    titel: str
    inhalt: str
    tags: list[str] = []

    @field_validator("titel")
    @classmethod
    def validate_titel(cls, value: str) -> str:
        """``titel`` must contain between 1 and 100 characters."""
        if not value or len(value) > TITEL_MAX_LENGTH:
            raise ValueError(f"titel must contain between 1 and {TITEL_MAX_LENGTH} characters")
        return value

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        """``tags`` must hold at most 5 entries."""
        if len(value) > TAGS_MAX_COUNT:
            raise ValueError(f"tags must contain at most {TAGS_MAX_COUNT} entries")
        return value


class Note(BaseModel):
    """A stored note, as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    titel: str
    inhalt: str
    tags: list[str]
    erstellt_am: datetime
