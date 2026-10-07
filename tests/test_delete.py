"""Tests for ``DELETE /notes/{note_id}``.

State is seeded directly through the shared store, not through ``POST /notes``
(which another ticket owns), so these tests stay independent of creation.

Remaining state is asserted through ``app.store.store`` — the single shared
in-memory store that ``GET /notes`` reads — because the read route is a
different ticket and is not implemented yet.
"""

from fastapi.testclient import TestClient

from app.store import store


def test_delete_existing_note_returns_204_and_removes_it(client: TestClient) -> None:
    first = store.create("Erste", "Inhalt eins", ["a"])
    second = store.create("Zweite", "Inhalt zwei", ["b"])

    response = client.delete(f"/notes/{first.id}")

    assert response.status_code == 204
    assert response.content == b""

    remaining_ids = [note.id for note in store.list()]
    assert first.id not in remaining_ids
    assert second.id in remaining_ids
    assert store.get(first.id) is None


def test_delete_unknown_id_returns_404_and_leaves_others_untouched(client: TestClient) -> None:
    first = store.create("Erste", "Inhalt eins", [])
    second = store.create("Zweite", "Inhalt zwei", [])

    response = client.delete("/notes/9999")

    assert response.status_code == 404
    assert [note.id for note in store.list()] == [first.id, second.id]


def test_deletion_keeps_remaining_ids_and_next_created_gets_fresh_id(client: TestClient) -> None:
    first = store.create("Erste", "Inhalt eins", [])
    second = store.create("Zweite", "Inhalt zwei", [])

    assert client.delete(f"/notes/{first.id}").status_code == 204

    remaining = store.list()
    assert [note.id for note in remaining] == [second.id]

    recreated = store.create("Dritte", "Inhalt drei", [])
    assert recreated.id != first.id
    assert recreated.id > second.id
