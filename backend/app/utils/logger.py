# backend/app/utils/logger.py

import logging
import sys
import json
from logging.handlers import RotatingFileHandler
from typing import Optional

from ..config import settings


# -----------------------------------------------------
# Цвета консоли
# -----------------------------------------------------

class ColorFormatter(logging.Formatter):
    """Красивый вывод логов в терминал (для DEV)."""

    COLORS = {
        "DEBUG": "\033[37m",   # white
        "INFO": "\033[36m",    # cyan
        "WARNING": "\033[33m", # yellow
        "ERROR": "\033[31m",   # red
        "CRITICAL": "\033[41m",# red bg
    }

    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        prefix = f"{color}{record.levelname}{self.RESET}"

        message = super().format(record)
        return f"[{prefix}] {message}"


# -----------------------------------------------------
# JSON форматтер (для продакшена)
# -----------------------------------------------------

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "level": record.levelname,
            "time": self.formatTime(record, self.datefmt),
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
        }
        return json.dumps(log, ensure_ascii=False)


# -----------------------------------------------------
# Создание логгера
# -----------------------------------------------------

def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # не создавать заново

    logger.setLevel(getattr(logging, settings.LOG_LEVEL))

    # -------------------------------------------------
    # Консольный хэндлер
    # -------------------------------------------------
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logger.level)

    if settings.LOG_JSON:
        console_handler.setFormatter(JsonFormatter())
    else:
        console_handler.setFormatter(
            ColorFormatter(
                "[%(asctime)s] %(name)s:%(lineno)d | %(message)s",
                datefmt="%H:%M:%S"
            )
        )

    logger.addHandler(console_handler)

    # -------------------------------------------------
    # Файловый хэндлер с ротацией
    # -------------------------------------------------
    if settings.LOG_TO_FILE:
        file_handler = RotatingFileHandler(
            filename=settings.LOG_FILE_PATH,
            maxBytes=settings.LOG_FILE_MAX_MB * 1024 * 1024,
            backupCount=settings.LOG_FILE_BACKUP_COUNT,
            encoding="utf-8"
        )
        file_handler.setLevel(logger.level)

        if settings.LOG_JSON:
            file_handler.setFormatter(JsonFormatter())
        else:
            file_handler.setFormatter(
                logging.Formatter(
                    "[%(asctime)s] %(levelname)s | %(name)s:%(lineno)d | %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
                )
            )

        logger.addHandler(file_handler)

    logger.propagate = False
    return logger


# -----------------------------------------------------
# Глобальная точка доступа
# -----------------------------------------------------

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Единая функция получения логгера в проекте."""
    return create_logger(name or "sentiment-analyzer")
