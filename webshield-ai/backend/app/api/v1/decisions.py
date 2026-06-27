from fastapi import APIRouter, Depends

from app.api.dependencies import get_policy_engine, get_settings_repository
from app.application.dto.decision_requests import ApplyPolicyInput
from app.application.use_cases.apply_policy import apply_policy
from app.domain.entities.user_preferences import UserPreferences
from app.domain.services.policy_engine import PolicyEngine
from app.infrastructure.repositories.settings_repository import SettingsRepository

router = APIRouter(prefix="/api/v1/decisions", tags=["decisions"])


@router.post("/preview")
def preview_decisions(
    payload: dict,
    engine: PolicyEngine = Depends(get_policy_engine),
    settings_repository: SettingsRepository = Depends(get_settings_repository),
):
    preferences = UserPreferences.model_validate(payload.get("preferences") or settings_repository.get().model_dump())
    decisions = [
        request_item
        for request_item in payload.get("decisions", [])
    ]
    from app.domain.entities.moderation_result import ContentDecision

    parsed = [ContentDecision.model_validate(item) for item in decisions]
    result = apply_policy(ApplyPolicyInput(decisions=parsed, preferences=preferences), engine)
    return {"decisions": result}
