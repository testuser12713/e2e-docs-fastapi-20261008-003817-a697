"""Shared pytest fixtures.

Every test starts from a clean store so tests stay independent of each other.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.store import store


@pytest.fixture(autouse=True)
def reset_store() -> None:
    """Clear the shared note store before each test."""
    store.clear()


@pytest.fixture
def client() -> TestClient:
    """A TestClient bound to the application under test."""
    return TestClient(app)
