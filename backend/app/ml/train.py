# backend/app/ml/train.py

import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import Adam
from typing import List

import pandas as pd

from .dataset import TextDataset
from .tokenizer import Tokenizer
from .model import SentimentModel, ModelHandler
from .metrics import compute_metrics
from ..utils.logger import get_logger

logger = get_logger(__name__)

# --------------------------------------------------------
# Функция загрузки данных
# --------------------------------------------------------
def load_data(train_path: str, max_len: int = 100):
    df = pd.read_csv(train_path)
    texts = df["text"].tolist()
    labels = df["label"].tolist()
    logger.info(f"Загружено {len(texts)} примеров из {train_path}")
    return texts, labels

# --------------------------------------------------------
# Функция подготовки DataLoader
# --------------------------------------------------------
def prepare_dataloader(texts: List[str], labels: List[int], tokenizer: Tokenizer, batch_size: int = 32, max_len: int = 100):
    dataset = TextDataset(texts=texts, labels=labels, tokenizer=tokenizer, max_len=max_len)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=dataset.collate_fn)
    return dataloader

# --------------------------------------------------------
# Основная функция обучения модели
# --------------------------------------------------------
def train_model(
    train_csv_path: str,
    save_model_path: str,
    vocab_path: str,
    embed_dim: int = 128,
    hidden_dim: int = 128,
    batch_size: int = 32,
    epochs: int = 5,
    lr: float = 1e-3,
    max_len: int = 100
):
    # ----------------------------
    # Загрузка данных
    # ----------------------------
    texts, labels = load_data(train_csv_path)

    # ----------------------------
    # Токенизация и построение словаря
    # ----------------------------
    tokenizer = Tokenizer(vocab_path=vocab_path)
    tokenizer.build_vocab(texts)
    tokenizer.save_vocab(vocab_path)

    # ----------------------------
    # DataLoader
    # ----------------------------
    dataloader = prepare_dataloader(texts, labels, tokenizer, batch_size=batch_size, max_len=max_len)

    # ----------------------------
    # Инициализация модели и оптимизатора
    # ----------------------------
    vocab_size = len(tokenizer.vocab) + 1  # +1 для padding_idx=0
    model = SentimentModel(vocab_size=vocab_size, embed_dim=embed_dim, hidden_dim=hidden_dim)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=lr)

    # ----------------------------
    # Цикл обучения
    # ----------------------------
    logger.info("Начало обучения модели...")
    for epoch in range(1, epochs + 1):
        model.train()
        epoch_loss = 0
        all_preds = []
        all_labels = []

        for batch in dataloader:
            input_ids = batch["input_ids"].to(device)
            batch_labels = batch["label"].to(device)

            optimizer.zero_grad()
            outputs = model(input_ids)
            loss = criterion(outputs, batch_labels)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            preds = torch.argmax(outputs, dim=1)
            all_preds.extend(preds.cpu().tolist())
            all_labels.extend(batch_labels.cpu().tolist())

        metrics = compute_metrics(all_preds, all_labels)
        logger.info(f"Epoch {epoch}/{epochs} | Loss: {epoch_loss/len(dataloader):.4f} | Metrics: {metrics}")

    # ----------------------------
    # Сохранение модели
    # ----------------------------
    handler = ModelHandler(model)
    handler.save_model(save_model_path)
    logger.info(f"Обучение завершено. Модель сохранена в {save_model_path}")

# --------------------------------------------------------
# Пример запуска
# --------------------------------------------------------
if __name__ == "__main__":
    train_csv = os.path.join(os.path.dirname(__file__), "../../data/train.csv")
    save_model = os.path.join(os.path.dirname(__file__), "../models/trained_model.pt")
    vocab_file = os.path.join(os.path.dirname(__file__), "../models/vocab.json")

    train_model(train_csv_path=train_csv, save_model_path=save_model, vocab_path=vocab_file)
