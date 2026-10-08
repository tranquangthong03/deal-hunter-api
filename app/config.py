"""
Application configuration.

Centralized settings loaded from environment variables with validation.
One source of truth for the entire application.
"""
from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ==================================================================
    # 1. APP
    # ==================================================================
    APP_NAME: str = "Deal Hunter API"
    APP_ENV: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = Field(..., min_length=16)

    # ==================================================================
    # 2. DATABASE
    # ==================================================================
    DATABASE_URL: PostgresDsn
    DB_POOL_SIZE: int = Field(default=10, ge=1, le=100)
    DB_MAX_OVERFLOW: int = Field(default=20, ge=0, le=100)
    DB_ECHO: bool = False

    # ==================================================================
    # 3. REDIS
    # ==================================================================
    REDIS_URL: RedisDsn
    CACHE_TTL_SECONDS: int = Field(default=300, ge=1)

    # ==================================================================
    # 4. CELERY
    # ==================================================================
    CELERY_BROKER_URL: RedisDsn
    CELERY_RESULT_BACKEND: RedisDsn

    # ==================================================================
    # 5. TELEGRAM
    # ==================================================================
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""

    # ==================================================================
    # 6. SCRAPER (Apify)
    # ==================================================================
    APIFY_API_TOKEN: str = ""
    APIFY_TIKI_ACTOR_ID: str = ""

    # ==================================================================
    # 7. BUSINESS LOGIC
    # ==================================================================
    CRAWL_INTERVAL_HOURS: int = Field(default=6, ge=1, le=24)
    DEAL_THRESHOLD_PERCENT: float = Field(default=15.0, ge=0, le=100)
    PRICE_HISTORY_LOOKBACK_DAYS: int = Field(default=7, ge=1, le=30)

    # ==================================================================
    # VALIDATORS
    # ==================================================================
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def ensure_async_driver(cls, v: str) -> str:
        """Force asyncpg driver — we only support async DB access."""
        if isinstance(v, str) and v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    # ==================================================================
    # COMPUTED PROPERTIES
    # ==================================================================
    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached settings instance — parsed only once per process."""
    return Settings()


# Module-level instance for convenience
settings = get_settings()