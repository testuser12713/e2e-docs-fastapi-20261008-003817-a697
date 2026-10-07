"""Tests for the note creation endpoint ``POST /notes``."""

from fastapi.testclient import TestClient


def _fields_with_error(response) -> set[str]:
    """Collect the field names named in a FastAPI 422 error body."""
    detail = response.json()["detail"]
    return {part for error in detail for part in error["loc"]}


def test_create_valid_note(client: TestClient) -> None:
    response = client.post(
        "/notes",
        json={"titel": "Einkauf", "inhalt": "Milch, Brot, Eier", "tags": ["a", "b", "c"]},
    )

    assert response.status_code == 201
    note = response.json()
    assert isinstance(note["id"], int)
    assert note["titel"] == "Einkauf"
    assert note["inhalt"] == "Milch, Brot, Eier"
    assert note["tags"] == ["a", "b", "c"]
    assert note["erstellt_am"]


def test_create_empty_titel_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/notes",
        json={"titel": "", "inhalt": "Inhalt", "tags": []},
    )

    assert response.status_code == 422
    assert "titel" in _fields_with_error(response)


def test_create_titel_too_long_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/notes",
        json={"titel": "x" * 101, "inhalt": "Inhalt", "tags": []},
    )

    assert response.status_code == 422
    assert "titel" in _fields_with_error(response)


def test_create_too_many_tags_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/notes",
        json={"titel": "Titel", "inhalt": "Inhalt", "tags": ["a", "b", "c", "d", "e", "f"]},
    )

    assert response.status_code == 422
    assert "tags" in _fields_with_error(response)
