from tests.fixtures.sample_pages import SAMPLE_PAGE
from tests.fixtures.sample_preferences import PREFERENCES


def test_page_analysis_returns_summary(client):
    payload = {**SAMPLE_PAGE, "preferences": PREFERENCES}
    response = client.post("/api/v1/moderation/page", json=payload)
    assert response.status_code == 200
    analysis = response.json()["analysis"]
    assert analysis["summary"]["url"] == SAMPLE_PAGE["url"]
    assert "safety_score" in analysis["summary"]
