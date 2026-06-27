from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_prefix="WEBSHIELD_",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "WebShield AI API"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True

    cors_allow_origins: list[str] = Field(default_factory=lambda: ["*"])

    text_toxicity_model: str = "unitary/toxic-bert"
    hate_speech_model: str = "facebook/roberta-hate-speech-dynabench-r4-target"
    nsfw_model: str = "Falconsai/nsfw_image_detection"
    violence_model: str = "jaranohaal/vit-base-violence-detection"
    embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    enable_remote_llm: bool = False
    llm_api_base: str = ""
    llm_api_key: str = ""
    llm_model_name: str = ""

    model_timeout_seconds: int = 20
    request_timeout_seconds: int = 10
    cache_ttl_seconds: int = 600

    max_text_items: int = 60
    max_image_items: int = 20
    max_promo_items: int = 20
    max_heading_items: int = 10

    storage_dir: Path = BASE_DIR / ".runtime"
    sqlite_path: Path = BASE_DIR / ".runtime" / "webshield.db"
    settings_path: Path = BASE_DIR / ".runtime" / "user_preferences.json"
    domain_rules_path: Path = BASE_DIR / ".runtime" / "domain_rules.json"

    data_dir: Path = BASE_DIR / "app" / "data"
    defaults_dir: Path = BASE_DIR / "app" / "data" / "defaults"

    def ensure_runtime_dirs(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)
        self.domain_rules_path.parent.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_runtime_dirs()
    return settings
