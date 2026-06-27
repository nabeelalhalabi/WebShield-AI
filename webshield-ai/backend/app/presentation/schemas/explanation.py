from pydantic import BaseModel, Field

from app.domain.entities.moderation_result import ContentDecision
from app.domain.entities.page_analysis import PreferenceMatch


class ExplanationRequest(BaseModel):
    title: str
    url: str
    safety_score: int
    preference_match: PreferenceMatch
    decisions: list[ContentDecision] = Field(default_factory=list)


class ExplanationResponse(BaseModel):
    explanation: str
