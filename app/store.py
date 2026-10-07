"""In-memory storage for notes.

The single shared state object every endpoint reads. Ids are ints, assigned
monotonically, and never reused: deleting a note leaves a gap the counter does
not step back into.
"""

from datetime import UTC, datetime

from app.schemas import Note


class InMemoryNoteStore:
    """A process-local, thread-unsafe note store backed by a dict."""

    def __init__(self) -> None:
        self._notes: dict[int, Note] = {}
        self._next_id: int = 1

    def create(self, titel: str, inhalt: str, tags: list[str]) -> Note:
        """Create and store a new note, returning the stored model."""
        note = Note(
            id=self._next_id,
            titel=titel,
            inhalt=inhalt,
            tags=list(tags),
            erstellt_am=datetime.now(UTC),
        )
        self._notes[note.id] = note
        self._next_id += 1
        return note

    def list(self, tag: str | None = None) -> list[Note]:
        """Return all notes, optionally only those carrying ``tag``."""
        notes = list(self._notes.values())
        if tag is not None:
            notes = [note for note in notes if tag in note.tags]
        return notes

    def get(self, note_id: int) -> Note | None:
        """Return the note with ``note_id`` or ``None`` when unknown."""
        return self._notes.get(note_id)

    def delete(self, note_id: int) -> bool:
        """Delete the note and return ``True``, or ``False`` when unknown."""
        return self._notes.pop(note_id, None) is not None

    def clear(self) -> None:
        """Remove every note and reset the id counter (test helper)."""
        self._notes.clear()
        self._next_id = 1


store = InMemoryNoteStore()
