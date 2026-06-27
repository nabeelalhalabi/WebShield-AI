from app.domain.entities.page_analysis import PageSummary
from app.infrastructure.repositories.history_repository import HistoryRepository


def save_page_history(summary: PageSummary, repository: HistoryRepository) -> None:
    repository.add(summary)
