# backend/app/config.py
import os
from pathlib import Path
from functools import lru_cache
from typing import List, Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Конфигурация backend-платформы анализа тональности.
    Загружается из .env + имеет безопасные fallback-значения.
    """

    # === Общие настройки ===
    ENV: str = Field(default="development", description="environment: development/production")
    DEBUG: bool = Field(default=True)

    # === API ===
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Sentiment Analyzer"
    VERSION: str = "0.1.0"

    # === CORS ===
    ALLOWED_ORIGINS: List[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "*",  # для MVP
        ]
    )

    # === Пути ===
    BASE_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2])
    BACKEND_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[1])

    DATA_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[1] / "data")
    MODELS_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[1] / "models")
    LOGS_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[1] / "logs")

    FRONTEND_DIST: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2] / "frontend" / "dist")

    # === Файлы модели ===
    MODEL_NAME: str = Field(default="distilbert-base-russian-sentiment")
    MODEL_PATH: Optional[Path] = None    # если скачана локально — путь будет помещён сюда
    TOKENIZER_PATH: Optional[Path] = None

    # === ML параметры ===
    DEVICE: str = Field(default="cpu", description="cpu или cuda для GPU-инференса")
    MAX_SEQ_LENGTH: int = Field(default=256)
    BATCH_SIZE: int = Field(default=16)

    # === Rate Limit (опционально) ===
    RATE_LIMIT_ENABLED: bool = Field(default=False)
    RATE_LIMIT_REQUESTS: int = Field(default=30)
    RATE_LIMIT_WINDOW: int = Field(default=60)  # сек

    # === Порог предсказаний ===
    CONFIDENCE_THRESHOLD: float = Field(default=0.55)

    # === Хранилище (опционально под расширение) ===
    USE_REDIS_CACHE: bool = Field(default=False)
    REDIS_URL: str = Field(default="redis://localhost:6379/0")

    USE_DATABASE: bool = Field(default=False)
    DATABASE_URL: str = Field(
        default="sqlite:///./sentiment.db",
        description="Может быть заменена на PostgreSQL: postgresql+asyncpg://user:pass@host/db",
    )

    # === Логи ===
    LOG_LEVEL: str = Field(default="INFO")
    LOG_TO_FILE: bool = Field(default=True)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Унифицированный доступ к настройкам
@lru_cache()
def get_settings() -> Settings:
    settings = Settings()

    # Создаём ключевые директории, если их нет
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # Уточняем пути к модели, если она уже скачана локально
    local_model_dir = settings.MODELS_DIR / settings.MODEL_NAME

    if local_model_dir.exists():
        settings.MODEL_PATH = local_model_dir
        settings.TOKENIZER_PATH = local_model_dir
    else:
        # Будет загружено динамически через transformers
        settings.MODEL_PATH = settings.MODEL_NAME
        settings.TOKENIZER_PATH = settings.MODEL_NAME

    return settings


# Единая точка импорта в других модулях:
settings = get_settings()
