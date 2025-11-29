# backend/app/core/search_engine.py

from typing import List, Optional
import pandas as pd

from .normalizer import Normalizer
from ..utils.logger import get_logger

logger = get_logger(__name__)

# --------------------------------------------------------
# Класс SearchEngine
# --------------------------------------------------------

class SearchEngine:
    """
    Поиск по текстам с использованием нормализованного индекса.
    - Поиск по ключевым словам
    - Фильтрация по источникам
    - Поддержка нормализованных текстов
    """

    def __init__(self, use_normalization: bool = True):
        self.use_normalization = use_normalization
        self.normalizer = Normalizer()
        self.df_index: Optional[pd.DataFrame] = None
        logger.info(f"SearchEngine инициализирован. use_normalization={self.use_normalization}")

    # ----------------------------------------------------
    # Построение индекса
    # ----------------------------------------------------
    def build_index(self, df: pd.DataFrame, text_column: str = "text") -> None:
        """
        Создает индекс для поиска по текстам
        """
        if text_column not in df.columns:
            raise ValueError(f"Отсутствует колонка для текста: {text_column}")

        self.df_index = df.copy()
        if self.use_normalization:
            self.df_index["norm_text"] = self.normalizer.normalize_list(self.df_index[text_column].tolist())
        else:
            self.df_index["norm_text"] = self.df_index[text_column]

        logger.info(f"Индекс построен. Размер: {len(self.df_index)} записей")

    # ----------------------------------------------------
    # Поиск по ключевым словам
    # ----------------------------------------------------
    def search(self, keywords: List[str], column: str = "norm_text") -> pd.DataFrame:
        """
        Возвращает DataFrame с текстами, содержащими хотя бы одно ключевое слово
        """
        if self.df_index is None:
            raise ValueError("Индекс не построен. Сначала вызовите build_index()")

        if not keywords:
            return self.df_index.copy()

        # Приведение ключевых слов к нижнему регистру и нормализация
        if self.use_normalization:
            keywords = [self.normalizer.normalize(word) for word in keywords]

        pattern = "|".join(keywords)
        df_filtered = self.df_index[self.df_index[column].str.contains(pattern, case=False, na=False)]

        logger.info(f"Поиск по ключевым словам {keywords}. Найдено: {len(df_filtered)} записей")
        return df_filtered

    # ----------------------------------------------------
    # Фильтрация по источникам
    # ----------------------------------------------------
    def filter_by_sources(self, sources: List[str], src_column: str = "src") -> pd.DataFrame:
        """
        Фильтрует DataFrame по источникам текстов
        """
        if self.df_index is None:
            raise ValueError("Индекс не построен. Сначала вызовите build_index()")

        if not sources:
            return self.df_index.copy()

        df_filtered = self.df_index[self.df_index[src_column].isin(sources)]
        logger.info(f"Фильтрация по источникам {sources}. Найдено: {len(df_filtered)} записей")
        return df_filtered
