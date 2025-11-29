# backend/tests/test_model.py

import pytest
import torch
from torch.utils.data import DataLoader

from backend.app.ml.model import ModelHandler
from backend.app.ml.dataset import TextDataset
from backend.app.ml.tokenizer import Tokenizer
from backend.app.ml.metrics import compute_metrics

# --------------------------------------------------------
# Тестирование ModelHandler
# --------------------------------------------------------

@pytest.fixture
def tokenizer():
    return Tokenizer()

@pytest.fixture
def sample_texts(tokenizer):
    texts = ["Пальто красивое, но пришло с дырой.", "Все отлично, качество супер!"]
    labels = [0, 2]
    dataset = TextDataset(texts=texts, labels=labels, tokenizer=tokenizer)
    return dataset

@pytest.fixture
def model_handler():
    handler = ModelHandler()
    return handler

def test_model_load(model_handler):
    """
    Проверка загрузки модели и device
    """
    assert hasattr(model_handler, "model"), "ModelHandler должен содержать model"
    assert model_handler.device in ["cpu", "cuda"], "device должен быть cpu или cuda"

def test_model_predict_returns_correct_length(model_handler, sample_texts):
    """
    Проверка, что predict возвращает список с тем же числом элементов, что и DataLoader
    """
    dataloader = DataLoader(sample_texts, batch_size=2, collate_fn=sample_texts.collate_fn)
    preds = model_handler.predict(dataloader)
    assert isinstance(preds, list), "predict должен возвращать список"
    assert len(preds) == len(sample_texts), "Количество предсказаний должно совпадать с количеством текстов"

def test_compute_metrics_matches_labels(model_handler, sample_texts):
    """
    Проверка метрик compute_metrics
    """
    dataloader = DataLoader(sample_texts, batch_size=2, collate_fn=sample_texts.collate_fn)
    preds = model_handler.predict(dataloader)
    labels = [label for _, label in sample_texts]
    metrics = compute_metrics(preds, labels)

    assert "macro_f1" in metrics, "metrics должны содержать ключ 'macro_f1'"
    assert "precision" in metrics, "metrics должны содержать ключ 'precision'"
    assert "recall" in metrics, "metrics должны содержать ключ 'recall'"
    assert 0.0 <= metrics["macro_f1"] <= 1.0, "macro_f1 должен быть между 0 и 1"
