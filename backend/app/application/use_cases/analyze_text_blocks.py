from app.application.dto.moderation_requests import AnalyzeTextBlocksInput
from app.application.dto.moderation_responses import AnalyzeTextBlocksOutput
from app.infrastructure.detectors.text_detector import TextDetector


def analyze_text_blocks(input_data: AnalyzeTextBlocksInput, detector: TextDetector) -> AnalyzeTextBlocksOutput:
    return AnalyzeTextBlocksOutput(decisions=detector.analyze_items(input_data.items))
