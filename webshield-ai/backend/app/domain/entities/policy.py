from pydantic import BaseModel, Field

from app.domain.value_objects.action_type import ActionType


class Policy(BaseModel):
    category_actions: dict[str, ActionType] = Field(default_factory=dict)
    thresholds: dict[str, float] = Field(default_factory=dict)
    child_safe_mode: bool = False
    default_action: ActionType = ActionType.WARN
