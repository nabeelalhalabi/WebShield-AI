from fastapi import APIRouter, Depends

from app.api.dependencies import get_explanation_engine
from app.application.dto.explanation_requests import GenerateExplanationInput
from app.application.use_cases.generate_explanation import generate_explanation
from app.domain.services.explanation_engine import ExplanationEngine
from app.presentation.schemas.explanation import ExplanationRequest, ExplanationResponse

router = APIRouter(prefix="/api/v1/explanations", tags=["explanations"])


@router.post("/generate", response_model=ExplanationResponse)
def generate_explanation_route(
    request: ExplanationRequest,
    engine: ExplanationEngine = Depends(get_explanation_engine),
):
    explanation = generate_explanation(
        GenerateExplanationInput(
            title=request.title,
            url=request.url,
            safety_score=request.safety_score,
            preference_match=request.preference_match,
            decisions=request.decisions,
        ),
        engine,
    )
    return ExplanationResponse(explanation=explanation)
