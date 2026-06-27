from functools import lru_cache

from app.config.settings import Settings, get_settings
from app.domain.rules.profanity_rules import ProfanityRules
from app.domain.rules.promo_rules import PromoRules
from app.domain.services.explanation_engine import ExplanationEngine
from app.domain.services.policy_engine import PolicyEngine
from app.domain.services.preference_similarity_engine import PreferenceSimilarityEngine
from app.domain.services.safety_score_engine import SafetyScoreEngine
from app.infrastructure.detectors.image_detector import ImageDetector
from app.infrastructure.detectors.profanity_detector import ProfanityDetector
from app.infrastructure.detectors.promo_detector import PromoDetector
from app.infrastructure.detectors.text_detector import TextDetector
from app.infrastructure.external.image_downloader import ImageDownloader
from app.infrastructure.external.llm_client import LLMClient
from app.infrastructure.model_providers.embeddings_provider import EmbeddingsProvider
from app.infrastructure.model_providers.explanation_provider import ExplanationProvider
from app.infrastructure.model_providers.hate_speech_provider import HateSpeechProvider
from app.infrastructure.model_providers.nsfw_provider import NsfwProvider
from app.infrastructure.model_providers.text_toxicity_provider import TextToxicityProvider
from app.infrastructure.model_providers.violence_provider import ViolenceProvider
from app.infrastructure.repositories.allowlist_repository import AllowlistRepository
from app.infrastructure.repositories.history_repository import HistoryRepository
from app.infrastructure.repositories.settings_repository import SettingsRepository
from app.infrastructure.storage.sqlite import SQLiteDatabase
from app.application.orchestrators.page_analysis_orchestrator import PageAnalysisOrchestrator


@lru_cache
def get_settings_repository() -> SettingsRepository:
    settings = get_settings()
    return SettingsRepository(
        defaults_path=settings.defaults_dir / "default_preferences.json",
        target_path=settings.settings_path,
    )


@lru_cache
def get_allowlist_repository() -> AllowlistRepository:
    settings = get_settings()
    return AllowlistRepository(settings.domain_rules_path)


@lru_cache
def get_history_repository() -> HistoryRepository:
    settings = get_settings()
    return HistoryRepository(SQLiteDatabase(settings.sqlite_path))


@lru_cache
def get_toxicity_provider() -> TextToxicityProvider:
    return TextToxicityProvider(get_settings())


@lru_cache
def get_hate_provider() -> HateSpeechProvider:
    return HateSpeechProvider(get_settings())


@lru_cache
def get_nsfw_provider() -> NsfwProvider:
    return NsfwProvider(get_settings())


@lru_cache
def get_violence_provider() -> ViolenceProvider:
    return ViolenceProvider(get_settings())


@lru_cache
def get_embeddings_provider() -> EmbeddingsProvider:
    return EmbeddingsProvider(get_settings())


@lru_cache
def get_profanity_detector() -> ProfanityDetector:
    settings = get_settings()
    rules = ProfanityRules(settings.defaults_dir / "banned_words.json")
    return ProfanityDetector(rules)


@lru_cache
def get_promo_detector() -> PromoDetector:
    settings = get_settings()
    rules = PromoRules(settings.defaults_dir / "promo_patterns.json")
    return PromoDetector(rules)


@lru_cache
def get_text_detector() -> TextDetector:
    return TextDetector(
        toxicity_provider=get_toxicity_provider(),
        hate_provider=get_hate_provider(),
        profanity_detector=get_profanity_detector(),
    )


@lru_cache
def get_image_detector() -> ImageDetector:
    settings = get_settings()
    return ImageDetector(
        downloader=ImageDownloader(settings),
        nsfw_provider=get_nsfw_provider(),
        violence_provider=get_violence_provider(),
    )


@lru_cache
def get_policy_engine() -> PolicyEngine:
    return PolicyEngine()


@lru_cache
def get_safety_score_engine() -> SafetyScoreEngine:
    settings = get_settings()
    return SafetyScoreEngine(settings.defaults_dir / "scoring_weights.json")


@lru_cache
def get_preference_engine() -> PreferenceSimilarityEngine:
    return PreferenceSimilarityEngine(get_embeddings_provider())


@lru_cache
def get_explanation_engine() -> ExplanationEngine:
    provider = ExplanationProvider(LLMClient(get_settings()))
    return ExplanationEngine(provider)


@lru_cache
def get_page_analysis_orchestrator() -> PageAnalysisOrchestrator:
    return PageAnalysisOrchestrator(
        text_detector=get_text_detector(),
        image_detector=get_image_detector(),
        promo_detector=get_promo_detector(),
        policy_engine=get_policy_engine(),
        safety_score_engine=get_safety_score_engine(),
        preference_engine=get_preference_engine(),
        explanation_engine=get_explanation_engine(),
        allowlist_repository=get_allowlist_repository(),
        history_repository=get_history_repository(),
    )
