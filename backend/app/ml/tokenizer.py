# backend/app/ml/tokenizer.py

from typing import List, Dict
import json
import os

from ..core.normalizer import Normalizer
from ..utils.logger import get_logger

logger = get_logger(__name__)

# --------------------------------------------------------
# Класс Tokenizer
# --------------------------------------------------------

class Tokenizer:
    """
    Токенизатор для платформы Sentiment Analyzer.
    - Создает словарь токенов (vocab)
    - Преобразует тексты в последовательности индексов
    - Может загружать и сохранять словарь
    """

    def __init__(self, vocab_path: str = None, remove_stopwords: bool = False):
        self.normalizer = Normalizer(remove_stopwords=remove_stopwords)
        self.vocab: Dict[str, int] = {}
        self.vocab_path = vocab_path
        if vocab_path and os.path.exists(vocab_path):
            self.load_vocab(vocab_path)
        logger.info(f"Tokenizer инициализирован. vocab_path={vocab_path}")

    # ----------------------------------------------------
    # Создание словаря по списку текстов
    # ----------------------------------------------------
    def build_vocab(self, texts: List[str], min_freq: int = 1):
        """
        Создает словарь токенов с минимальной частотой
        """
        token_freq: Dict[str, int] = {}
        for text in texts:
            tokens = self.normalizer._tokenize(text)
            for token in tokens:
                token_freq[token] = token_freq.get(token, 0) + 1

        # Отбираем токены по минимальной частоте
        self.vocab = {token: idx for idx, (token, freq) in enumerate(token_freq.items()) if freq >= min_freq}
        logger.info(f"Словарь построен. Размер: {len(self.vocab)} токенов")

    # ----------------------------------------------------
    # Преобразование текста в последовательность индексов
    # ----------------------------------------------------
    def text_to_sequence(self, text: str, max_len: int = 100) -> List[int]:
        tokens = self.normalizer._tokenize(text)
        sequence = [self.vocab.get(token, 0) for token in tokens]  # 0 для неизвестных токенов
        # Ограничение длины
        if len(sequence) > max_len:
            sequence = sequence[:max_len]
        else:
            sequence += [0] * (max_len - len(sequence))
        return sequence

    # ----------------------------------------------------
    # Batch преобразование
    # ----------------------------------------------------
    def texts_to_sequences(self, texts: List[str], max_len: int = 100) -> List[List[int]]:
        return [self.text_to_sequence(text, max_len=max_len) for text in texts]

    # ----------------------------------------------------
    # Сохранение словаря
    # ----------------------------------------------------
    def save_vocab(self, path: str = None):
        path = path or self.vocab_path
        if not path:
            raise ValueError("Не указан путь для сохранения словаря")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.vocab, f, ensure_ascii=False, indent=2)
        logger.info(f"Словарь сохранен: {path}")

    # ----------------------------------------------------
    # Загрузка словаря
    # ----------------------------------------------------
    def load_vocab(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            self.vocab = json.load(f)
        logger.info(f"Словарь загружен: {path}")
