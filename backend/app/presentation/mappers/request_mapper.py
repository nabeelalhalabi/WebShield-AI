from app.common.enums import ContentKind
from app.domain.entities.content_item import ContentItem
from app.domain.entities.user_preferences import UserPreferences
from app.presentation.schemas.page import PageAnalysisRequest


def _to_text_item(payload: dict) -> ContentItem:
    return ContentItem(
        item_id=payload["item_id"],
        kind=ContentKind.TEXT,
        text=payload.get("text"),
        tag_name=payload.get("tag_name"),
        page_url=payload.get("page_url"),
        meta=payload.get("meta", {}),
    )


def _to_image_item(payload: dict) -> ContentItem:
    return ContentItem(
        item_id=payload["item_id"],
        kind=ContentKind.IMAGE,
        source_url=payload.get("src"),
        alt_text=payload.get("alt_text"),
        tag_name=payload.get("tag_name"),
        page_url=payload.get("page_url"),
        meta={"width": payload.get("width"), "height": payload.get("height"), **payload.get("meta", {})},
    )


def _to_promo_item(payload: dict) -> ContentItem:
    return ContentItem(
        item_id=payload["item_id"],
        kind=ContentKind.PROMOTION,
        text=payload.get("text"),
        tag_name=payload.get("tag_name"),
        role=payload.get("role"),
        class_name=payload.get("class_name"),
        page_url=payload.get("page_url"),
        meta=payload.get("meta", {}),
    )


def _to_heading_item(payload: dict) -> ContentItem:
    return ContentItem(
        item_id=payload["item_id"],
        kind=ContentKind.HEADING,
        text=payload.get("text"),
        tag_name=f"h{payload.get('level', 1)}",
        page_url=payload.get("page_url"),
        meta=payload.get("meta", {}),
    )


def map_page_request_to_input(request: PageAnalysisRequest, preferences: UserPreferences):
    from app.application.dto.moderation_requests import AnalyzePageInput

    return AnalyzePageInput(
        url=request.url,
        title=request.title,
        text_items=[_to_text_item(item) for item in request.text_items],
        image_items=[_to_image_item(item) for item in request.image_items],
        promo_items=[_to_promo_item(item) for item in request.promo_items],
        heading_items=[_to_heading_item(item) for item in request.headings],
        preferences=preferences,
    )
