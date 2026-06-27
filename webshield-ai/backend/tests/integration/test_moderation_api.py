from tests.fixtures.sample_preferences import PREFERENCES


def test_text_moderation_endpoint(client):
    response = client.post(
        "/api/v1/moderation/text",
        json={
            "items": [{"item_id": "t-1", "text": "You are disgusting and stupid."}],
            "preferences": PREFERENCES,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["results"]
