from app.application.dto.moderation_requests import AnalyzeImagesInput
from app.application.dto.moderation_responses import AnalyzeImagesOutput
from app.domain.services.policy_engine import PolicyEngine
from app.infrastructure.detectors.image_detector import ImageDetector


def analyze_images(
    input_data: AnalyzeImagesInput,
    detector: ImageDetector,
    policy_engine: PolicyEngine,
) -> AnalyzeImagesOutput:
    raw_decisions = detector.analyze_items(input_data.items)
    final_decisions = policy_engine.apply(raw_decisions, input_data.preferences)
    return AnalyzeImagesOutput(decisions=final_decisions)