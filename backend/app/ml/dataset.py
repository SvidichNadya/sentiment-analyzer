# backend/app/ml/dataset.py

from typing import List, Optional
import torch
from torch.utils.data import Dataset

from .tokenizer import Tokenizer
from ..core.normalizer import Normalizer
from ..utils.logger import get_logger

logger = get_logger(__name__)

# --------------------------------------------------------
# Класс TextDataset
# --------------------------------------------------------

class TextDataset(Dataset):
    """
    PyTorch Dataset для текстов с тональностью
    Поддерживает:
    - Токенизацию и нормализацию
    - Конвертацию текста в последовательность индексов
    - Возврат метки для обучения
    """

    def __init__(self, texts: List[str], labels: Optional[List[int]] = None, tokenizer: Optional[Tokenizer] = None, max_len: int = 100):
        self.texts = texts
        self.labels = labels
        self.max_len = max_len

        if tokenizer is None:
            self.tokenizer = Tokenizer()
        else:
            self.tokenizer = tokenizer

        logger.info(f"TextDataset инициализирован. Кол-во примеров: {len(self.texts)}")

    # ----------------------------------------------------
    # Длина датасета
    # ----------------------------------------------------
    def __len__(self):
        return len(self.texts)

    # ----------------------------------------------------
    # Получение одного примера
    # ----------------------------------------------------
    def __getitem__(self, idx):
        text = self.texts[idx]
        input_ids = torch.tensor(self.tokenizer.text_to_sequence(text, max_len=self.max_len), dtype=torch.long)

        if self.labels is not None:
            label = torch.tensor(self.labels[idx], dtype=torch.long)
            return {"input_ids": input_ids, "label": label}
        else:
            return {"input_ids": input_ids}

    # ----------------------------------------------------
    # Генерация всего батча (для DataLoader)
    # ----------------------------------------------------
    def collate_fn(self, batch):
        input_ids = torch.stack([item["input_ids"] for item in batch])
        if "label" in batch[0]:
            labels = torch.stack([item["label"] for item in batch])
            return {"input_ids": input_ids, "labels": labels}
        return {"input_ids": input_ids}
