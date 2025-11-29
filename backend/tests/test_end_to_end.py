# backend/tests/test_end_to_end.py

import os
import pytest
import pandas as pd
from fastapi.testclient import TestClient
from torch.utils.data import DataLoader

from backend.app.main import app
from backend.app.ml.model import ModelHandler
from backend.app.ml.dataset import TextDataset
from backend.app.ml.tokenizer import Tokenizer
from backend.app.ml.metrics import compute_metrics
from backend.app.core.normalizer import Normalizer

client = TestClient(app)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "../app/data/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --------------------------------------------------------
# Энд-то-энд тест: загрузка CSV, предсказание и метрики
# --------------------------------------------------------
def test_end_to_end_pipeline(tmp_path):
    # 1️⃣ Создание тестового CSV
    df = pd.DataFrame({
        "text": ["Пальто красивое, но пришло с дырой", "Все отлично, качество супер!"],
        "label": [0, 2],
        "src": ["rureviews", "rureviews"]
    })
    test_file = tmp_path / "test.csv"
    df.to_csv(test_file, index=False)

    # 2️⃣ Загрузка CSV через API
    with open(test_file, "rb") as f:
        response = client.post("/upload/csv", files={"file": ("test.csv", f, "text/csv")})
    assert response.status_code == 200

    # 3️⃣ Чтение CSV и нормализация
    uploaded_file = os.path.join(UPLOAD_DIR, "test.csv")
    df_uploaded = pd.read_csv(uploaded_file)
    normalizer = Normalizer()
    df_uploaded["tokens"] = df_uploaded["text"].apply(lambda x: normalizer.normalize(x))

    # 4️⃣ Подготовка датасета и DataLoader
    tokenizer = Tokenizer()
    dataset = TextDataset(df_uploaded["text"].tolist(), df_uploaded["label"].tolist(), tokenizer)
    dataloader = DataLoader(dataset, batch_size=2, collate_fn=dataset.collate_fn)

    # 5️⃣ Предсказания модели
    model_handler = ModelHandler()
    predictions = model_handler.predict(dataloader)

    # 6️⃣ Вычисление метрик
    labels = df_uploaded["label"].tolist()
    metrics = compute_metrics(predictions, labels)

    # ✅ Проверки
    assert len(predictions) == len(df_uploaded), "Количество предсказаний должно совпадать с количеством текстов"
    assert 0.0 <= metrics["macro_f1"] <= 1.0, "macro_f1 должен быть в диапазоне 0-1"
    assert all(k in metrics for k in ["precision", "recall", "macro_f1"]), "Метрики должны содержать precision, recall, macro_f1"
