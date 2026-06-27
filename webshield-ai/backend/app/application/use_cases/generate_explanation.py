from app.application.dto.explanation_requests import GenerateExplanationInput
from app.domain.services.explanation_engine import ExplanationEngine


def generate_explanation(input_data: GenerateExplanationInput, engine: ExplanationEngine) -> str:
    return engine.build(
        title=input_data.title,
        url=input_data.url,
        safety_score=input_data.safety_score,
        decisions=input_data.decisions,
        preference_match=input_data.preference_match,
    )
