# backend/app/core/preprocessing.py

from typing import List
import re
import pandas as pd

from ..utils.logger import get_logger
from ..utils.csv_tools import normalize_csv_columns
from .normalizer import Normalizer

logger = get_logger(__name__)

# --------------------------------------------------------
# Основной класс PreprocessingPipeline
# --------------------------------------------------------

class PreprocessingPipeline:
    """
    Класс для предобработки текстов перед обучением и инференсом.
    Объединяет стандартные NLP шаги:
    - очистка текста
    - токенизация
    - лемматизация
    - Named Entity Recognition (опционально)
    """

    def __init__(self, use_ner: bool = False):
        self.normalizer = Normalizer()
        self.use_ner = use_ner
        logger.info(f"PreprocessingPipeline инициализирован. use_ner={self.use_ner}")

    # ----------------------------------------------------
    # Основной метод предобработки DataFrame
    # ----------------------------------------------------
    def process_dataframe(self, df: pd.DataFrame, text_column: str = "text") -> pd.DataFrame:
        """
        Применяет пайплайн ко всем текстам в DataFrame
        """
        df = normalize_csv_columns(df)
        if text_column not in df.columns:
            raise ValueError(f"Отсутствует колонка для текста: {text_column}")

        df["clean_text"] = df[text_column].apply(self.process_text)
        logger.info(f"DataFrame предобработан. Количество строк: {len(df)}")
        return df

    # ----------------------------------------------------
    # Предобработка одного текста
    # ----------------------------------------------------
    def process_text(self, text: str) -> str:
        """
        Основные шаги предобработки текста:
        - очистка от спецсимволов
        - нормализация (токенизация, лемматизация)
        - опционально извлечение именованных сущностей
        """
        if not isinstance(text, str):
            text = str(text)

        # Очистка текста
        text = self._clean_text(text)

        # NLP нормализация
        text = self.normalizer.normalize(text)

        # Можно добавить NER или другие шаги, если use_ner=True
        if self.use_ner:
            text = self._apply_ner(text)

        return text

    # ----------------------------------------------------
    # Внутренние методы
    # ----------------------------------------------------
    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Очистка текста:
        - убираем URL
        - убираем спецсимволы
        - приводим к нижнему регистру
        """
        text = text.lower()
        text = re.sub(r"http\S+|www\S+", "", text)  # убираем ссылки
        text = re.sub(r"[^а-яА-Яa-zA-Z0-9\s]", " ", text)  # оставляем буквы и цифры
        text = re.sub(r"\s+", " ", text)  # удаляем лишние пробелы
        return text.strip()

    def _apply_ner(self, text: str) -> str:
        """
        Применение NER (Named Entity Recognition).
        Пока заглушка — можно расширить с использованием spacy, Natasha и т.д.
        """
        # Для MVP можно возвращать текст без изменений
        return text


# --------------------------------------------------------
# Удобная функция для быстрого вызова
# --------------------------------------------------------
def preprocess_texts(texts: List[str], use_ner: bool = False) -> List[str]:
    """
    Быстрая функция предобработки списка текстов
    """
    pipeline = PreprocessingPipeline(use_ner=use_ner)
    return [pipeline.process_text(text) for text in texts]
