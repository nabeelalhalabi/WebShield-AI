from typing import Any

from pydantic import BaseModel, Field

from app.domain.value_objects.action_type import ActionType
from app.domain.value_objects.risk_label import RiskLabel


class ModuleSignal(BaseModel):
    category: str
    label: str
    confidence: float = 0.0
    risk_level: RiskLabel = RiskLabel.SAFE
    reason: str = ""
    matched_rules: list[str] = Field(default_factory=list)
    raw_scores: dict[str, float] = Field(default_factory=dict)
    model_name: str | None = None
    provider_status: str = "ok"


class ContentDecision(BaseModel):
    item_id: str
    content_kind: str
    action: ActionType = ActionType.ALLOW
    risk_level: RiskLabel = RiskLabel.SAFE
    confidence: float = 0.0
    explanation: str = ""
    categories: list[str] = Field(default_factory=list)
    primary_category: str | None = None
    module_results: list[ModuleSignal] = Field(default_factory=list)
    meta: dict[str, Any] = Field(default_factory=dict)
