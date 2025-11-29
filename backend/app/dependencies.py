# backend/app/dependencies.py

import time
import asyncio
from functools import lru_cache
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, Request, status

from .config import settings
from .utils.logger import get_logger
from .core.preprocessing import Preprocessor
from .core.normalizer import TextNormalizer
from .core.search_engine import SearchEngine
from .ml.model import SentimentModel


# -------------------------
# Глобальный логгер
# -------------------------
logger = get_logger(__name__)


# -------------------------
# Lazy-кэш для модели
# -------------------------

class ModelContainer:
    """
    Синглтон-контейнер.
    Хранит загруженную модель и инструменты пайплайна.
    """

    def __init__(self):
        self.model: Optional[SentimentModel] = None
        self.preprocessor: Optional[Preprocessor] = None
        self.normalizer: Optional[TextNormalizer] = None
        self.search_engine: Optional[SearchEngine] = None

    def is_loaded(self) -> bool:
        return self.model is not None


container = ModelContainer()


# -------------------------
# Инициализация кэша (Redis или in-memory)
# -------------------------

class LocalCache:
    """Простой in-memory cache для MVP."""

    def __init__(self):
        self.store: Dict[str, Any] = {}

    def get(self, key: str):
        return self.store.get(key)

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        self.store[key] = value

    def exists(self, key: str) -> bool:
        return key in self.store


if settings.USE_REDIS_CACHE:
    import redis.asyncio as redis
    redis_client = redis.from_url(settings.REDIS_URL)
else:
    redis_client = LocalCache()


# -------------------------
# Rate Limiting (MVP)
# -------------------------

class RateLimiter:
    def __init__(self, limit: int, window: int):
        self.limit = limit
        self.window = window

    async def check(self, request: Request):
        if not settings.RATE_LIMIT_ENABLED:
            return

        key = f"rl:{request.client.host}"
        current = await self._get(key)
        if current is None:
            await self._set(key, 1)
            return

        if current >= self.limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )

        await self._set(key, current + 1)

    async def _get(self, key: str) -> Optional[int]:
        if isinstance(redis_client, LocalCache):
            return redis_client.get(key)
        val = await redis_client.get(key)
        return int(val) if val else None

    async def _set(self, key: str, value: int):
        if isinstance(redis_client, LocalCache):
            redis_client.set(key, value)
        else:
            await redis_client.set(key, value, ex=settings.RATE_LIMIT_WINDOW)


rate_limiter = RateLimiter(
    limit=settings.RATE_LIMIT_REQUESTS,
    window=settings.RATE_LIMIT_WINDOW
)


async def rate_limit_dependency(request: Request):
    """Подключается как Depends() в публичных ручках."""
    await rate_limiter.check(request)


# -------------------------
# Загрузка модели и NLP-пайплайна
# -------------------------

@lru_cache()
def load_pipeline():
    """
    Функция вызывается один раз при старте приложения.
    Загружает:
      - модель
      - tokenizer
      - preprocessor
      - normalizer
      - search index
    """

    logger.info("Загрузка NLP-пайплайна...")

    # Нормализация текста
    normalizer = TextNormalizer()

    # Препроцессинг (очистка, токены)
    preprocessor = Preprocessor(normalizer=normalizer)

    # Модель тональности
    model = SentimentModel(
        model_path=settings.MODEL_PATH,
        tokenizer_path=settings.TOKENIZER_PATH,
        device=settings.DEVICE,
        max_length=settings.MAX_SEQ_LENGTH,
        confidence_threshold=settings.CONFIDENCE_THRESHOLD,
    )

    # Поисковый индекс
    search_engine = SearchEngine(normalizer=normalizer)

    logger.info("Пайплайн успешно загружен")

    return {
        "model": model,
        "preprocessor": preprocessor,
        "normalizer": normalizer,
        "search_engine": search_engine,
    }


def init_container():
    """
    Запускается из main.py при старте приложения.
    Заполняет глобальный контейнер.
    """

    if container.is_loaded():
        return

    assets = load_pipeline()
    container.model = assets["model"]
    container.preprocessor = assets["preprocessor"]
    container.normalizer = assets["normalizer"]
    container.search_engine = assets["search_engine"]

    logger.info("Глобальный контейнер NLP-пайплайна инициализирован.")


# -------------------------
# Dependencies для FastAPI
# -------------------------

def get_model() -> SentimentModel:
    """Dependency для инференса."""
    if not container.is_loaded():
        init_container()
    return container.model


def get_preprocessor() -> Preprocessor:
    if not container.is_loaded():
        init_container()
    return container.preprocessor


def get_normalizer() -> TextNormalizer:
    if not container.is_loaded():
        init_container()
    return container.normalizer


def get_search_engine() -> SearchEngine:
    if not container.is_loaded():
        init_container()
    return container.search_engine


def get_cache():
    """Dependency для записи результатов анализа."""
    return redis_client


def get_logger_dep():
    return logger


# -------------------------
# Health check зависимости
# -------------------------

async def check_health():
    """
    Проверяет состояние модели и кэша.
    Используется в /api/health.
    """
    if not container.is_loaded():
        init_container()

    ok = {"model": True, "cache": True}

    if settings.USE_REDIS_CACHE:
        try:
            pong = await redis_client.ping()
            ok["cache"] = pong is True
        except Exception:
            ok["cache"] = False

    return ok
