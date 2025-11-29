# backend/app/utils/csv_tools.py

import pandas as pd
from typing import List, Optional

from .logger import get_logger
from ..config import settings

logger = get_logger(__name__)

# --------------------------------------------------------------------
# Обязательные колонки для платформы
# --------------------------------------------------------------------
REQUIRED_COLUMNS = ["text", "label", "src"]


# --------------------------------------------------------------------
# Функция нормализации названий колонок
# --------------------------------------------------------------------
def normalize_csv_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Унифицирует названия колонок:
    - приводит к lower-case
    - убирает пробелы
    - переименовывает синонимы к стандарту
    """
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]

    # Переименование возможных альтернатив
    rename_map = {
        "review": "text",
        "comment": "text",
        "rating": "label",
        "source": "src"
    }

    df.rename(columns=rename_map, inplace=True)

    logger.debug(f"Колонки после нормализации: {df.columns.tolist()}")
    return df


# --------------------------------------------------------------------
# Валидация наличия обязательных колонок
# --------------------------------------------------------------------
def validate_required_columns(df: pd.DataFrame) -> List[str]:
    """
    Проверяет наличие обязательных колонок.
    Возвращает список отсутствующих колонок.
    """
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        logger.warning(f"Отсутствуют обязательные колонки: {missing}")
    return missing


# --------------------------------------------------------------------
# Сохранение DataFrame в CSV с опциональной нормализацией
# --------------------------------------------------------------------
def save_dataframe_to_csv(df: pd.DataFrame, path: str, normalize: bool = True) -> None:
    """
    Сохраняет DataFrame в CSV.
    Если normalize=True, сначала нормализует колонки.
    """
    if normalize:
        df = normalize_csv_columns(df)

    df.to_csv(path, index=False, encoding="utf-8")
    logger.info(f"DataFrame сохранён в CSV: {path}")


# --------------------------------------------------------------------
# Универсальная функция подготовки данных для ML
# --------------------------------------------------------------------
def prepare_dataset_for_ml(df: pd.DataFrame, require_label: bool = True) -> pd.DataFrame:
    """
    Преобразует DataFrame для подачи в ML-модель:
    - нормализация колонок
    - проверка обязательных полей
    - фильтрация пустых текстов
    """
    df = normalize_csv_columns(df)

    missing_cols = validate_required_columns(df)
    if require_label and "label" in missing_cols:
        raise ValueError("DataFrame не содержит обязательную колонку 'label'")
    if "text" in missing_cols:
        raise ValueError("DataFrame не содержит обязательную колонку 'text'")

    # Удаляем пустые тексты
    df = df[df["text"].notna() & (df["text"].str.strip() != "")]
    df = df.reset_index(drop=True)

    logger.info(f"DataFrame подготовлен для ML. Размер: {df.shape}")
    return df


# --------------------------------------------------------------------
# Поиск текста по ключевым словам
# --------------------------------------------------------------------
def filter_texts_by_keyword(df: pd.DataFrame, keywords: List[str], column: str = "text") -> pd.DataFrame:
    """
    Возвращает DataFrame с текстами, содержащими хотя бы одно ключевое слово
    """
    df_filtered = df[df[column].str.contains("|".join(keywords), case=False, na=False)]
    logger.debug(f"Фильтр по ключевым словам {keywords}. Найдено: {df_filtered.shape[0]} записей")
    return df_filtered
