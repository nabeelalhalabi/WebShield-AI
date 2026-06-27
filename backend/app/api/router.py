from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.moderation import router as moderation_router
from app.api.v1.preferences import router as preferences_router
from app.api.v1.decisions import router as decisions_router
from app.api.v1.explanations import router as explanations_router
from app.api.v1.history import router as history_router

router = APIRouter()
router.include_router(health_router)
router.include_router(moderation_router)
router.include_router(preferences_router)
router.include_router(decisions_router)
router.include_router(explanations_router)
router.include_router(history_router)
