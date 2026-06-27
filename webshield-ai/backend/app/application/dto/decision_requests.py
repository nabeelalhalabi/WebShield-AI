from pydantic import BaseModel, Field

from app.domain.entities.moderation_result import ContentDecision
from app.domain.entities.user_preferences import UserPreferences


class ApplyPolicyInput(BaseModel):
    decisions: list[ContentDecision] = Field(default_factory=list)
    preferences: UserPreferences
