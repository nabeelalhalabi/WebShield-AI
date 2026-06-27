from fastapi import APIRouter

from app.api.dependencies import (
    get_embeddings_provider,
    get_hate_provider,
    get_nsfw_provider,
    get_toxicity_provider,
    get_violence_provider,
)
from app.common.utils.time_utils import iso_now

router = APIRouter(prefix="/api/v1/health", tags=["health"])


@router.get("")
def health_check():
    providers = [
        get_toxicity_provider().health(),
        get_hate_provider().health(),
        get_nsfw_provider().health(),
        get_violence_provider().health(),
        get_embeddings_provider().health(),
    ]
    return {"status": "ok", "time": iso_now(), "providers": providers}
