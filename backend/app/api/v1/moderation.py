from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import (
    get_image_detector,
    get_page_analysis_orchestrator,
    get_policy_engine,
    get_promo_detector,
    get_settings,
    get_settings_repository,
    get_text_detector,
)
from app.application.dto.moderation_requests import (
    AnalyzeImagesInput,
    AnalyzePageInput,
    AnalyzePromotionsInput,
    AnalyzeTextBlocksInput,
)
from app.application.use_cases.analyze_images import analyze_images
from app.application.use_cases.analyze_page import analyze_page
from app.application.use_cases.analyze_promotions import analyze_promotions
from app.application.use_cases.analyze_text_blocks import analyze_text_blocks
from app.common.exceptions import ValidationError
from app.common.security.input_validation import validate_counts, validate_page_url
from app.config.settings import Settings
from app.domain.entities.content_item import ContentItem
from app.domain.entities.user_preferences import UserPreferences
from app.domain.services.policy_engine import PolicyEngine
from app.infrastructure.detectors.image_detector import ImageDetector
from app.infrastructure.detectors.promo_detector import PromoDetector
from app.infrastructure.detectors.text_detector import TextDetector
from app.infrastructure.repositories.settings_repository import SettingsRepository
from app.application.orchestrators.page_analysis_orchestrator import PageAnalysisOrchestrator
from app.presentation.mappers.request_mapper import map_page_request_to_input
from app.presentation.mappers.response_mapper import map_image_results, map_page_output, map_text_results
from app.presentation.schemas.image import ImageModerationRequest
from app.presentation.schemas.page import PageAnalysisRequest
from app.presentation.schemas.text import TextModerationRequest

router = APIRouter(prefix="/api/v1/moderation", tags=["moderation"])


def _resolve_preferences(
    provided: UserPreferences | None,
    repository: SettingsRepository,
) -> UserPreferences:
    return provided or repository.get()


@router.post("/text")
def moderate_text(
    request: TextModerationRequest,
    detector: TextDetector = Depends(get_text_detector),
):
    items = [
        ContentItem(
            item_id=item.item_id,
            kind="text",
            text=item.text,
            tag_name=item.tag_name,
            page_url=item.page_url,
            meta=item.meta,
        )
        for item in request.items
    ]
    output = analyze_text_blocks(
        AnalyzeTextBlocksInput(items=items, preferences=request.preferences),
        detector,
    )
    return map_text_results(output.decisions)


@router.post("/images")
def moderate_images(
    request: ImageModerationRequest,
    detector: ImageDetector = Depends(get_image_detector),
    policy_engine: PolicyEngine = Depends(get_policy_engine),
):
    items = [
        ContentItem(
            item_id=item.item_id,
            kind="image",
            source_url=item.src,
            alt_text=item.alt_text,
            tag_name=item.tag_name,
            page_url=item.page_url,
            meta={"width": item.width, "height": item.height, **item.meta},
        )
        for item in request.items
    ]
    output = analyze_images(
        AnalyzeImagesInput(items=items, preferences=request.preferences),
        detector,
        policy_engine,
    )
    return map_image_results(output.decisions)


@router.post("/promotions")
def moderate_promotions(
    payload: dict,
    detector: PromoDetector = Depends(get_promo_detector),
):
    preferences = UserPreferences.model_validate(payload["preferences"])
    items = [
        ContentItem(
            item_id=item["item_id"],
            kind="promotion",
            text=item["text"],
            tag_name=item.get("tag_name"),
            role=item.get("role"),
            class_name=item.get("class_name"),
            page_url=item.get("page_url"),
            meta=item.get("meta", {}),
        )
        for item in payload.get("items", [])
    ]
    return analyze_promotions(AnalyzePromotionsInput(items=items, preferences=preferences), detector)


@router.post("/page")
def moderate_page(
    request: PageAnalysisRequest,
    orchestrator: PageAnalysisOrchestrator = Depends(get_page_analysis_orchestrator),
    repository: SettingsRepository = Depends(get_settings_repository),
    settings: Settings = Depends(get_settings),
):
    try:
        validate_page_url(request.url)
        validate_counts(
            text_items=len(request.text_items),
            image_items=len(request.image_items),
            promo_items=len(request.promo_items),
            max_text_items=settings.max_text_items,
            max_image_items=settings.max_image_items,
            max_promo_items=settings.max_promo_items,
        )
        preferences = _resolve_preferences(request.preferences, repository)
        mapped = map_page_request_to_input(request, preferences)
        output = analyze_page(mapped, orchestrator)
        return map_page_output(output)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc