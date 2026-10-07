"""Tests for the note read endpoints (listing, tag filter, single fetch)."""

from fastapi.testclient import TestClient

from app.store import store


def _seed() -> None:
    """Seed two notes directly through the store, independent of POST /notes."""
    store.create(titel="First", inhalt="Body one", tags=["work", "urgent"])
    store.create(titel="Second", inhalt="Body two", tags=["home"])


def test_list_returns_every_note(client: TestClient) -> None:
    _seed()

    response = client.get("/notes")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert [note["titel"] for note in body] == ["First", "Second"]


def test_list_filter_by_tag_returns_only_matching(client: TestClient) -> None:
    _seed()

    response = client.get("/notes", params={"tag": "work"})

    assert response.status_code == 200
    body = response.json()
    assert [note["titel"] for note in body] == ["First"]
    assert body[0]["tags"] == ["work", "urgent"]


def test_list_filter_by_unknown_tag_returns_empty_list(client: TestClient) -> None:
    _seed()

    response = client.get("/notes", params={"tag": "missing"})

    assert response.status_code == 200
    assert response.json() == []


def test_get_by_known_id_returns_that_note(client: TestClient) -> None:
    _seed()

    response = client.get("/notes/1")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["titel"] == "First"
    assert body["inhalt"] == "Body one"
    assert body["tags"] == ["work", "urgent"]


def test_get_unknown_id_returns_404(client: TestClient) -> None:
    _seed()

    response = client.get("/notes/999")

    assert response.status_code == 404
