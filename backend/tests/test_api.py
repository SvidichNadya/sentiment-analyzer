# backend/tests/test_api.py

import os
import pytest
import pandas as pd
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "../app/data/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --------------------------------------------------------
# Тест эндпоинта /upload/csv
# --------------------------------------------------------
def test_upload_csv_file(tmp_path):
    # Создаем тестовый CSV файл
    df = pd.DataFrame({"text": ["Тестовый отзыв"]})
    test_file = tmp_path / "test.csv"
    df.to_csv(test_file, index=False)

    with open(test_file, "rb") as f:
        response = client.post("/upload/csv", files={"file": ("test.csv", f, "text/csv")})

    assert response.status_code == 200
    assert "Файл успешно загружен" in response.json()["message"]

# --------------------------------------------------------
# Тест эндпоинта /search/texts
# --------------------------------------------------------
def test_search_texts():
    response = client.get("/search/texts", params={"query": "Пальто"})
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert data["query"] == "Пальто"
    assert "results" in data
    assert isinstance(data["results"], list)

# --------------------------------------------------------
# Тест эндпоинта /admin/files
# --------------------------------------------------------
def test_admin_list_files():
    response = client.get("/admin/files")
    assert response.status_code == 200
    data = response.json()
    assert "files" in data
    assert isinstance(data["files"], list)

# --------------------------------------------------------
# Тест эндпоинта /admin/file
# --------------------------------------------------------
def test_admin_get_file(tmp_path):
    # Создаем тестовый CSV
    df = pd.DataFrame({"text": ["Тестовый отзыв"]})
    file_name = "admin_test.csv"
    test_file = tmp_path / file_name
    df.to_csv(test_file, index=False)

    # Копируем в папку uploads
    dest = os.path.join(UPLOAD_DIR, file_name)
    df.to_csv(dest, index=False)

    response = client.get("/admin/file", params={"file_name": file_name})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert data["data"][0]["text"] == "Тестовый отзыв"
