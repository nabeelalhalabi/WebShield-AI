from pydantic import BaseModel, Field, field_validator

from app.domain.value_objects.action_type import ActionType


class DetectorToggles(BaseModel):
    toxicity: bool = True
    profanity: bool = True
    hate_speech: bool = True
    nsfw: bool = True
    violence: bool = True
    promotions: bool = True
    preference_match: bool = True
    explanations: bool = True


class UserPreferences(BaseModel):
    enabled: bool = True
    child_safe_mode: bool = False
    scan_on_load: bool = True
    history_enabled: bool = True

    interests: list[str] = Field(default_factory=list)
    detectors: DetectorToggles = Field(default_factory=DetectorToggles)

    thresholds: dict[str, float] = Field(default_factory=dict)
    category_actions: dict[str, ActionType | str] = Field(default_factory=dict)

    allowlist: list[str] = Field(default_factory=list)
    blocklist: list[str] = Field(default_factory=list)

    max_text_items: int = 40
    max_image_items: int = 12
    max_promo_items: int = 12

    @field_validator("thresholds")
    @classmethod
    def clamp_thresholds(cls, values: dict[str, float]) -> dict[str, float]:
        return {key: max(0.0, min(1.0, float(value))) for key, value in values.items()}

    @field_validator("category_actions")
    @classmethod
    def normalize_actions(cls, values: dict[str, ActionType | str]) -> dict[str, ActionType]:
        normalized: dict[str, ActionType] = {}
        for key, value in values.items():
            normalized[key] = value if isinstance(value, ActionType) else ActionType(value)
        return normalized
