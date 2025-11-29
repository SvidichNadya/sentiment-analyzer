# backend/app/core/normalizer.py

from typing import List
import re

import pymorphy2
from ..utils.logger import get_logger

logger = get_logger(__name__)

# --------------------------------------------------------
# Класс Normalizer
# --------------------------------------------------------

class Normalizer:
    """
    Нормализатор текста:
    - токенизация
    - лемматизация
    - удаление стоп-слов (опционально)
    """

    def __init__(self, remove_stopwords: bool = False, custom_stopwords: List[str] = None):
        self.morph = pymorphy2.MorphAnalyzer()
        self.remove_stopwords = remove_stopwords
        self.stopwords = set(custom_stopwords) if custom_stopwords else set()
        logger.info(f"Normalizer инициализирован. remove_stopwords={self.remove_stopwords}")

    # ----------------------------------------------------
    # Основной метод нормализации текста
    # ----------------------------------------------------
    def normalize(self, text: str) -> str:
        """
        Нормализация текста:
        1. Очистка и токенизация
        2. Лемматизация каждого токена
        3. Удаление стоп-слов (если включено)
        """
        if not isinstance(text, str):
            text = str(text)

        tokens = self._tokenize(text)
        lemmas = [self._lemmatize(token) for token in tokens]

        if self.remove_stopwords:
            lemmas = [lemma for lemma in lemmas if lemma not in self.stopwords]

        normalized_text = " ".join(lemmas)
        return normalized_text

    # ----------------------------------------------------
    # Токенизация текста
    # ----------------------------------------------------
    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """
        Разделяет текст на токены, оставляя только буквы и цифры
        """
        tokens = re.findall(r"\b\w+\b", text.lower())
        return tokens

    # ----------------------------------------------------
    # Лемматизация токена
    # ----------------------------------------------------
    def _lemmatize(self, token: str) -> str:
        """
        Возвращает нормальную форму слова с помощью pymorphy2
        """
        lemma = self.morph.parse(token)[0].normal_form
        return lemma

    # ----------------------------------------------------
    # Вспомогательный метод: пакетная нормализация
    # ----------------------------------------------------
    def normalize_list(self, texts: List[str]) -> List[str]:
        """
        Нормализация списка текстов
        """
        return [self.normalize(text) for text in texts]
