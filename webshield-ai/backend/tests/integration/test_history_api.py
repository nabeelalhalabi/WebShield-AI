from fastapi.testclient import TestClient


def test_history_initially_returns_items_wrapper(client: TestClient) -> None:
    response = client.get("/api/v1/history")
    response.raise_for_status()
    payload = response.json()
    assert isinstance(payload, dict)
    assert "items" in payload
    assert isinstance(payload["items"], list)
