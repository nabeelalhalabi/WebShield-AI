from app.application.dto.moderation_responses import AnalyzePageOutput
from app.presentation.schemas.page import PageAnalysisResponse
from app.presentation.schemas.text import TextModerationResponse
from app.presentation.schemas.image import ImageModerationResponse


def map_page_output(output: AnalyzePageOutput) -> PageAnalysisResponse:
    return PageAnalysisResponse(analysis=output.analysis)


def map_text_results(results):
    return TextModerationResponse(results=results)


def map_image_results(results):
    return ImageModerationResponse(results=results)
