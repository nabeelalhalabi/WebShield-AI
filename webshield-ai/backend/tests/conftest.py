import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api import dependencies


@pytest.fixture(autouse=True)
def force_fallback_providers(monkeypatch):
    def make_fallback(provider_getter):
        provider = provider_getter()
        monkeypatch.setattr(provider, "_load", lambda: provider._mark_fallback("forced-test-fallback"))
        if hasattr(provider, "_pipeline"):
            provider._pipeline = None
        if hasattr(provider, "_model"):
            provider._model = None

    make_fallback(dependencies.get_toxicity_provider)
    make_fallback(dependencies.get_hate_provider)
    make_fallback(dependencies.get_nsfw_provider)
    make_fallback(dependencies.get_violence_provider)
    make_fallback(dependencies.get_embeddings_provider)
    yield


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client
