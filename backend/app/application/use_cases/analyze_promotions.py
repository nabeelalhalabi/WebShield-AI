from app.application.dto.moderation_requests import AnalyzePromotionsInput
from app.application.dto.moderation_responses import AnalyzePromotionsOutput
from app.infrastructure.detectors.promo_detector import PromoDetector


def analyze_promotions(
    input_data: AnalyzePromotionsInput,
    detector: PromoDetector,
) -> AnalyzePromotionsOutput:
    return AnalyzePromotionsOutput(decisions=detector.analyze_items(input_data.items))
