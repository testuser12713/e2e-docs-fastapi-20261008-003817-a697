"""Note creation route: ``POST /notes``."""

from fastapi import APIRouter, status

from app.schemas import Note, NoteCreate
from app.store import store

router = APIRouter()


@router.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(payload: NoteCreate) -> Note:
    """Create a note from a validated payload and return the stored note."""
    return store.create(titel=payload.titel, inhalt=payload.inhalt, tags=payload.tags)
