from fastapi import APIRouter, Depends

from app.api.dependencies import get_history_repository
from app.infrastructure.repositories.history_repository import HistoryRepository

router = APIRouter(prefix="/api/v1/history", tags=["history"])


@router.get("")
def list_history(
    limit: int = 50,
    repository: HistoryRepository = Depends(get_history_repository),
):
    return {"items": repository.list(limit=limit)}


@router.delete("")
def clear_history(repository: HistoryRepository = Depends(get_history_repository)):
    repository.clear()
    return {"status": "cleared"}
