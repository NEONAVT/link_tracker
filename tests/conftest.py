import os
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Disable Sentry during tests BEFORE importing the app
os.environ.setdefault("SENTRY_DSN", "")

# Ensure project root on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from main import app as _app
from services.link_service import LinkService
from repository.link_repository import LinkRepository
from dependency import get_link_service

# If Sentry middleware wraps the FastAPI app, unwrap to get the real FastAPI instance
app = getattr(_app, "app", _app)

class InMemoryRepository(LinkRepository):
    # Simple in-memory repository implementation for tests.
    def __init__(self):
        self._items = []  # list of (timestamp, domain)

    def add_domains(self, domains: list[str], timestamp: int) -> None:
        for d in domains:
            self._items.append((timestamp, d))

    def get_domains_in_interval(self, start: int, end: int) -> list[str]:
        result = [d for ts, d in self._items if start <= ts <= end]
        return sorted(set(result))

@pytest.fixture()
def repo():
    return InMemoryRepository()

@pytest.fixture()
def test_app(repo):
    # Build a service from in-memory repository and override dependency
    service = LinkService(repository=repo)

    def _override_get_link_service():
        return service

    app.dependency_overrides[get_link_service] = _override_get_link_service
    yield app
    app.dependency_overrides.clear()

@pytest.fixture()
def client(test_app):
    return TestClient(test_app)
