from pydantic import BaseModel, Field

from app.domain.entities.moderation_result import ContentDecision
from app.domain.entities.page_analysis import PageAnalysis


class AnalyzeTextBlocksOutput(BaseModel):
    decisions: list[ContentDecision] = Field(default_factory=list)


class AnalyzeImagesOutput(BaseModel):
    decisions: list[ContentDecision] = Field(default_factory=list)


class AnalyzePromotionsOutput(BaseModel):
    decisions: list[ContentDecision] = Field(default_factory=list)


class AnalyzePageOutput(BaseModel):
    analysis: PageAnalysis
