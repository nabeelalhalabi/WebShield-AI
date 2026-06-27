from fastapi import APIRouter, Depends

from app.api.dependencies import get_allowlist_repository, get_settings_repository
from app.infrastructure.repositories.allowlist_repository import AllowlistRepository
from app.infrastructure.repositories.settings_repository import SettingsRepository
from app.presentation.schemas.preferences import PreferencesResponse, PreferencesUpdateRequest

router = APIRouter(prefix="/api/v1/preferences", tags=["preferences"])


@router.get("", response_model=PreferencesResponse)
def get_preferences(repository: SettingsRepository = Depends(get_settings_repository)):
    return PreferencesResponse(preferences=repository.get())


@router.put("", response_model=PreferencesResponse)
def update_preferences(
    request: PreferencesUpdateRequest,
    repository: SettingsRepository = Depends(get_settings_repository),
    allowlist_repository: AllowlistRepository = Depends(get_allowlist_repository),
):
    saved = repository.save(request)
    allowlist_repository.save_rules(allowlist=saved.allowlist, blocklist=saved.blocklist)
    return PreferencesResponse(preferences=saved)
