"""Note read routes: ``GET /notes`` and ``GET /notes/{note_id}``."""

from fastapi import APIRouter, HTTPException

from app.schemas import Note
from app.store import store

router = APIRouter()


@router.get("/notes", response_model=list[Note])
async def list_notes(tag: str | None = None) -> list[Note]:
    """Return every note, optionally restricted to those carrying ``tag``."""
    return store.list(tag)


@router.get("/notes/{note_id}", response_model=Note)
async def get_note(note_id: int) -> Note:
    """Return the note with ``note_id`` or answer 404 when it is unknown."""
    note = store.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
