"""Note deletion route: ``DELETE /notes/{note_id}``.

The handler body is an inert stub owned by the deletion ticket.
"""

from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int) -> None:
    raise HTTPException(status_code=501, detail="Not implemented")
