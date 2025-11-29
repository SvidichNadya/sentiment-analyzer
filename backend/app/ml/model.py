import os
from typing import List, Optional, Dict

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from .dataset import TextDataset
from .metrics import compute_metrics
from ..utils.logger import get_logger
from .. import config

logger = get_logger(__name__)

# --------------------------------------------------------
# Модель для классификации тональности
# --------------------------------------------------------

class SentimentModel(nn.Module):
    def __init__(self, vocab_size: int, embed_dim: int = 128, hidden_dim: int = 128, output_dim: int = 3):
        super(SentimentModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, output_dim)
        self.softmax = nn.Softmax(dim=1)
        logger.info(f"SentimentModel инициализирована. vocab_size={vocab_size}, embed_dim={embed_dim}, hidden_dim={hidden_dim}")

    def forward(self, input_ids):
        x = self.embedding(input_ids)
        lstm_out, _ = self.lstm(x)
        out = lstm_out[:, -1, :]
        logits = self.fc(out)
        probs = self.softmax(logits)
        return probs

# --------------------------------------------------------
# Класс для управления моделью
# --------------------------------------------------------

class ModelHandler:
    def __init__(self, model: nn.Module, device: Optional[str] = None):
        # Используем DEVICE из config.py, если device не передан
        self.device = device or config.settings.DEVICE or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = model.to(self.device)
        self.model.eval()
        logger.info(f"ModelHandler инициализирован. Device={self.device}")

    # ----------------------------------------------------
    # Сохранение модели
    # ----------------------------------------------------
    def save_model(self, path: Optional[str] = None):
        path = path or os.environ.get("MODEL_PATH", str(config.settings.MODELS_DIR / "trained_model.pt"))
        torch.save(self.model.state_dict(), path)
        logger.info(f"Модель сохранена: {path}")

    # ----------------------------------------------------
    # Загрузка модели
    # ----------------------------------------------------
    def load_model(self, path: Optional[str] = None):
        path = path or os.environ.get("MODEL_PATH", str(config.settings.MODELS_DIR / "trained_model.pt"))
        self.model.load_state_dict(torch.load(path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
        logger.info(f"Модель загружена: {path}")

    # ----------------------------------------------------
    # Инференс для списка текстов
    # ----------------------------------------------------
    def predict(self, dataloader: DataLoader) -> List[int]:
        self.model.eval()
        preds = []
        with torch.no_grad():
            for batch in dataloader:
                input_ids = batch["input_ids"].to(self.device)
                outputs = self.model(input_ids)
                batch_preds = torch.argmax(outputs, dim=1).cpu().tolist()
                preds.extend(batch_preds)
        return preds

    # ----------------------------------------------------
    # Оценка модели
    # ----------------------------------------------------
    def evaluate(self, dataloader: DataLoader, labels: List[int]) -> Dict[str, float]:
        preds = self.predict(dataloader)
        metrics = compute_metrics(preds, labels)
        logger.info(f"Оценка модели: {metrics}")
        return metrics
