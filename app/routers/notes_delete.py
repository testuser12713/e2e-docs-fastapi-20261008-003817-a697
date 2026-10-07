"""Note deletion route: ``DELETE /notes/{note_id}``."""

from fastapi import APIRouter, HTTPException, status

from app.store import store

router = APIRouter()


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int) -> None:
    """Delete a note by id, or answer 404 when the id is unknown."""
    if not store.delete(note_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
