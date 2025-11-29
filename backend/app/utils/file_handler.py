# backend/app/utils/file_handler.py

import os
import uuid
import shutil
import pandas as pd
from pathlib import Path
from typing import Optional, Union, List

from fastapi import UploadFile, HTTPException

from ..config import settings
from .logger import get_logger
from .csv_tools import normalize_csv_columns, validate_required_columns


logger = get_logger(__name__)


# --------------------------------------------------------------------
# Пути и системные директории
# --------------------------------------------------------------------

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

TEMP_DIR = Path(settings.TEMP_DIR)
TEMP_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------
# Валидация расширений
# --------------------------------------------------------------------

ALLOWED_EXTENSIONS = {".csv", ".txt", ".json"}

def validate_extension(filename: str):
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        logger.warning(f"Попытка загрузки недопустимого файла: {filename}")
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимый тип файла: {ext}. Разрешено: {ALLOWED_EXTENSIONS}"
        )


# --------------------------------------------------------------------
# Генерация безопасного имени файла
# --------------------------------------------------------------------

def generate_safe_filename(original_name: str) -> str:
    ext = Path(original_name).suffix
    new_name = f"{uuid.uuid4().hex}{ext}"
    logger.debug(f"Сгенерировано безопасное имя файла: {new_name}")
    return new_name


# --------------------------------------------------------------------
# Сохранение загруженного файла
# --------------------------------------------------------------------

def save_uploaded_file(file: UploadFile) -> Path:
    validate_extension(file.filename)

    safe_name = generate_safe_filename(file.filename)
    file_path = UPLOAD_DIR / safe_name

    logger.info(f"Сохранение файла: {file.filename} → {file_path}")

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


# --------------------------------------------------------------------
# Чтение CSV / TXT / JSON в DataFrame
# --------------------------------------------------------------------

def load_to_dataframe(path: Union[str, Path]) -> pd.DataFrame:
    path = Path(path)
    ext = path.suffix.lower()

    logger.debug(f"Чтение файла в DataFrame: {path}")

    if ext == ".csv":
        df = pd.read_csv(path)
    elif ext == ".txt":
        df = pd.read_csv(path, sep="\n", header=None, names=["text"])
    elif ext == ".json":
        df = pd.read_json(path)
    else:
        raise HTTPException(400, f"Неподдерживаемый формат файла: {ext}")

    # нормализация колонок, подготовка к дальнейшей обработке
    df = normalize_csv_columns(df)

    logger.info(f"Файл загружен. Размер: {df.shape}")
    return df


# --------------------------------------------------------------------
# Проверка обязательных колонок
# --------------------------------------------------------------------

def ensure_required_columns(df: pd.DataFrame):
    missing = validate_required_columns(df)
    if missing:
        raise HTTPException(
            400,
            f"Отсутствуют обязательные столбцы: {missing}"
        )


# --------------------------------------------------------------------
# Временные файлы
# --------------------------------------------------------------------

def save_temp_dataframe(df: pd.DataFrame, prefix: str = "tmp_") -> Path:
    filename = prefix + uuid.uuid4().hex + ".csv"
    temp_path = TEMP_DIR / filename

    df.to_csv(temp_path, index=False, encoding="utf-8")
    logger.debug(f"Временный CSV создан: {temp_path}")

    return temp_path


def cleanup_temp_files(max_age_minutes: int = 30) -> int:
    """Удаляет временные файлы старше max_age_minutes."""
    deleted = 0
    now = pd.Timestamp.now()

    for file in TEMP_DIR.iterdir():
        if not file.is_file():
            continue

        mtime = pd.Timestamp(file.stat().st_mtime)
        age = (now - mtime).total_seconds() / 60

        if age > max_age_minutes:
            file.unlink(missing_ok=True)
            deleted += 1
            logger.debug(f"Удалён временный файл: {file}")

    if deleted:
        logger.info(f"Очистка временных файлов завершена: {deleted} шт.")

    return deleted


# --------------------------------------------------------------------
# API-ориентированные методы
# --------------------------------------------------------------------

def handle_file_upload(file: UploadFile) -> pd.DataFrame:
    """
    Универсальная функция:
    • сохраняет файл
    • загружает в DataFrame
    • нормализует
    • проверяет обязательные колонки
    """
    path = save_uploaded_file(file)
    df = load_to_dataframe(path)
    ensure_required_columns(df)

    logger.info(f"Файл валидирован и готов к обработке: {path}")
    return df


def write_output_csv(df: pd.DataFrame, filename: Optional[str] = None) -> Path:
    """Сохранение результата инференса в output-файл."""
    fname = filename or f"results_{uuid.uuid4().hex}.csv"
    out_path = UPLOAD_DIR / fname

    df.to_csv(out_path, index=False, encoding="utf-8")

    logger.info(f"Результат обработки сохранён: {out_path}")
    return out_path
