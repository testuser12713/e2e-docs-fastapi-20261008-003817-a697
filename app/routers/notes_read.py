"""Note read routes: ``GET /notes`` and ``GET /notes/{note_id}``.

The handler bodies are inert stubs owned by the read ticket.
"""

from fastapi import APIRouter, HTTPException

from app.schemas import Note

router = APIRouter()


@router.get("/notes", response_model=list[Note])
async def list_notes(tag: str | None = None) -> list[Note]:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/notes/{note_id}", response_model=Note)
async def get_note(note_id: int) -> Note:
    raise HTTPException(status_code=501, detail="Not implemented")
