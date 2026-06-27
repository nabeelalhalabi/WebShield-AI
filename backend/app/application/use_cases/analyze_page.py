from app.application.dto.moderation_requests import AnalyzePageInput
from app.application.dto.moderation_responses import AnalyzePageOutput
from app.application.orchestrators.page_analysis_orchestrator import PageAnalysisOrchestrator


def analyze_page(input_data: AnalyzePageInput, orchestrator: PageAnalysisOrchestrator) -> AnalyzePageOutput:
    return AnalyzePageOutput(analysis=orchestrator.analyze(input_data))
