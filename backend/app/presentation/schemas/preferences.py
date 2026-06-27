from pydantic import BaseModel

from app.domain.entities.user_preferences import UserPreferences


class PreferencesResponse(BaseModel):
    preferences: UserPreferences


class PreferencesUpdateRequest(UserPreferences):
    pass
