from app.domain.entities.user_preferences import UserPreferences
from app.domain.services.preference_similarity_engine import score_preference_similarity


def calculate_preference_match(page_text: str, preferences: UserPreferences) -> dict[str, object]:
    """Calculate how closely a page matches the user's interests."""
    similarity, matches = score_preference_similarity(page_text, preferences)
    return {"similarity": similarity, "matches": matches}
