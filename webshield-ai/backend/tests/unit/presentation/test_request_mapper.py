from app.domain.entities.user_preferences import UserPreferences
from app.presentation.mappers.request_mapper import map_page_request_to_input
from app.presentation.schemas.page import PageAnalysisRequest


def test_request_mapper_builds_items():
    request = PageAnalysisRequest(
        url="https://example.com",
        title="Example",
        text_items=[{"item_id": "t1", "text": "hello"}],
        image_items=[],
        promo_items=[],
        headings=[],
    )
    mapped = map_page_request_to_input(request, UserPreferences())
    assert mapped.url == "https://example.com"
    assert len(mapped.text_items) == 1
