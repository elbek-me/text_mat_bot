"""Ilova sozlamalari (.env yoki muhit o'zgaruvchilaridan o'qiladi)."""
from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    bot_token: SecretStr
    log_level: str = "INFO"
    log_dir: Path = BASE_DIR / "logs"
    font_path: Path = BASE_DIR / "assets" / "fonts" / "handwriting.ttf"

    max_handwriting_chars: int = Field(6000, gt=0)
    max_tts_chars: int = Field(2000, gt=0)
    max_translate_chars: int = Field(4000, gt=0)
    max_pages: int = Field(10, gt=0, le=10)  # Telegram albomi 10 tagacha
    throttle_seconds: float = Field(1.0, ge=0)


@lru_cache
def get_settings() -> Settings:
    return Settings()
