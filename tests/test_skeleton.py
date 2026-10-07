"""Tests for the service skeleton: app wiring, health, settings and the store.

These cover only what the skeleton itself delivers. The note endpoint
behaviours are owned by their own tickets and are deliberately not asserted
here.
"""

from fastapi.testclient import TestClient

from app.config import Settings, settings
from app.main import app
from app.store import store


def test_app_is_importable() -> None:
    assert app.title == settings.app_name


def test_health_returns_ok_and_app_name(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app_name": settings.app_name}


def test_settings_load_defaults_without_env(monkeypatch) -> None:
    monkeypatch.delenv("APP_NAME", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    fresh = Settings()
    assert fresh.app_name == "Notes API"
    assert fresh.log_level == "INFO"


def test_store_create_assigns_id_and_timestamp() -> None:
    note = store.create("First", "Body", ["work"])
    assert note.id == 1
    assert note.titel == "First"
    assert note.inhalt == "Body"
    assert note.tags == ["work"]
    assert note.erstellt_am is not None


def test_store_get_returns_none_for_unknown_id() -> None:
    assert store.get(123) is None


def test_store_list_and_tag_filter() -> None:
    store.create("First", "Body", ["work", "urgent"])
    store.create("Second", "Body", ["home"])

    assert len(store.list()) == 2
    assert [note.titel for note in store.list("work")] == ["First"]
    assert store.list("missing") == []


def test_store_delete_keeps_remaining_ids_stable() -> None:
    first = store.create("First", "Body", [])
    second = store.create("Second", "Body", [])

    assert store.delete(first.id) is True
    assert store.get(first.id) is None
    assert store.delete(first.id) is False
    assert store.delete(999) is False

    assert [note.id for note in store.list()] == [second.id]

    third = store.create("Third", "Body", [])
    assert third.id == 3
