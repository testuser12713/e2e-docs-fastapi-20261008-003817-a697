"""Note creation route: ``POST /notes``.

The handler body is an inert stub owned by the note-creation ticket.
"""

from fastapi import APIRouter, HTTPException, status

from app.schemas import Note, NoteCreate

router = APIRouter()


@router.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(payload: NoteCreate) -> Note:
    raise HTTPException(status_code=501, detail="Not implemented")
