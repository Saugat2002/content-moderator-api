from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional, List
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    # API Configuration
    API_KEY: str = os.getenv("API_KEY", "")
    API_KEY_NAME: str = "X-API-Key"

    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Content Analysis Configuration
    POSITIVE_WORDS: List[str] = [
        "good",
        "great",
        "excellent",
        "love",
        "happy",
        "wonderful",
        "amazing",
        "fantastic",
        "best",
        "perfect",
    ]
    NEGATIVE_WORDS: List[str] = [
        "bad",
        "terrible",
        "awful",
        "hate",
        "sad",
        "worst",
        "horrible",
        "disappointing",
        "poor",
        "negative",
    ]
    TOXIC_WORDS: List[str] = [
        "bad",
        "terrible",
        "awful",
        "hate",
        "stupid",
        "idiot",
        "dumb",
        "worthless",
        "useless",
        "trash",
    ]

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
