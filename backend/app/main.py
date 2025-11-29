# backend/app/main.py
import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# Локальные модули — будут реализованы отдельными файлами
from app.core import evaluation  # noqa: F401  (модуль метрик, нужен позже)
from app.utils import logger
from app import config
from app import dependencies

# Routers (будут реализованы в app/api/*.py)
try:
    from app.api.routes_prediction import router as prediction_router
except Exception:
    prediction_router = None

try:
    from app.api.routes_validation import router as validation_router
except Exception:
    validation_router = None

try:
    from app.api.routes_upload import router as upload_router
except Exception:
    upload_router = None

try:
    from app.api.routes_search import router as search_router
except Exception:
    search_router = None

try:
    from app.api.routes_admin import router as admin_router
except Exception:
    admin_router = None


LOG = logger.get_logger(__name__)


def create_app() -> FastAPI:
    """
    Создаёт и настраивает FastAPI приложение.
    Регистрация роутеров вынесена сюда, чтобы было легко тестировать и использовать в Gunicorn/Uvicorn.
    """
    app = FastAPI(
        title="Sentiment Analyzer",
        description="API сервиса анализа тональности русскоязычных отзывов",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Middlewares
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # CORS: для MVP разрешаем основные origin'ы через конфиг
    origins = config.ALLOWED_ORIGINS if hasattr(config, "ALLOWED_ORIGINS") else ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Static files: если есть собранный frontend (frontend/dist), монтируем
    try:
        frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
        if frontend_dist.exists():
            app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
            LOG.info("Mounted frontend static files from %s", frontend_dist)
        else:
            LOG.debug("Frontend dist not found at %s — skipping static mount", frontend_dist)
    except Exception as e:
        LOG.exception("Error while mounting static files: %s", e)

    # Include routers if они реализованы
    if prediction_router is not None:
        app.include_router(prediction_router, prefix="/api/predict", tags=["prediction"])
        LOG.debug("Registered prediction router")
    else:
        LOG.warning("Prediction router is not available — /api/predict disabled")

    if validation_router is not None:
        app.include_router(validation_router, prefix="/api/validate", tags=["validation"])
        LOG.debug("Registered validation router")

    if upload_router is not None:
        app.include_router(upload_router, prefix="/api/upload", tags=["upload"])
        LOG.debug("Registered upload router")

    if search_router is not None:
        app.include_router(search_router, prefix="/api/search", tags=["search"])
        LOG.debug("Registered search router")

    if admin_router is not None:
        app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
        LOG.debug("Registered admin router")

    # Health & readiness
    @app.get("/health", tags=["health"])
    def health() -> dict:
        """Simple healthcheck endpoint."""
        return {"status": "ok"}

    @app.get("/ready", tags=["health"])
    def ready() -> dict:
        """
        Readiness probe: проверяем, загружена ли модель и инициализированы ресурсы.
        dependencies.has_model_loaded() должен быть реализован в dependencies.py.
        """
        try:
            loaded = False
            if hasattr(dependencies, "has_model_loaded"):
                loaded = dependencies.has_model_loaded()
            return {"ready": loaded}
        except Exception as e:
            LOG.exception("Readiness check failed: %s", e)
            return JSONResponse(status_code=500, content={"ready": False, "error": str(e)})

    # Global exception handler — возвращаем JSON с ошибкой
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        LOG.exception("Unhandled exception for request %s: %s", request.url.path, exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "error": str(exc)},
        )

    # Startup / Shutdown events
    @app.on_event("startup")
    async def on_startup() -> None:
        LOG.info("Starting application (startup event)")
        # Инициализируем логгер (если требуется)
        try:
            logger.configure_logging()
        except Exception:
            # logger.configure_logging может быть опциональным
            pass

        # Загружаем необходимые ресурсы (модель, токенизатор и т.д.)
        try:
            if hasattr(dependencies, "initialize"):
                # ожидаем, что dependencies.initialize занимается загрузкой модели и других ресурсов
                maybe_coro = dependencies.initialize()
                if hasattr(maybe_coro, "__await__"):
                    # if initialize is async
                    await maybe_coro
                LOG.info("Dependencies initialized")
            else:
                LOG.warning("dependencies.initialize not implemented — skipping resource initialization")
        except Exception as e:
            LOG.exception("Failed to initialize dependencies: %s", e)
            # не прерываем стартап полностью — readiness/health покажут проблему

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        LOG.info("Shutting down application (shutdown event)")
        if hasattr(dependencies, "shutdown"):
            try:
                maybe_coro = dependencies.shutdown()
                if hasattr(maybe_coro, "__await__"):
                    await maybe_coro
                LOG.info("Dependencies shutdown complete")
            except Exception:
                LOG.exception("Error during dependencies.shutdown()")

    return app


app = create_app()


if __name__ == "__main__":
    # Запуск через uvicorn при локальной разработке
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        log_level=os.getenv("UVICORN_LOG_LEVEL", "info"),
        # reload=True  # включаем в dev-скриптах, но не по умолчанию в production
    )