# backend/app/api/routes_upload.py

from fastapi import APIRouter, UploadFile, File
import os
import pandas as pd
from datetime import datetime
from ..utils.file_handler import save_uploaded_file
from ..utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/upload", tags=["Upload"])

# --------------------------------------------------------
# Эндпоинт: загрузка CSV-файла с отзывами
# --------------------------------------------------------
@router.post("/csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Загружает CSV-файл с отзывами на сервер.
    Ожидается колонка 'text'.
    Сохраняет файл в директорию backend/app/data/uploads/
    """
    if not file.filename.endswith(".csv"):
        return {"error": "Только CSV файлы поддерживаются"}

    contents = await file.read()
    df = pd.read_csv(pd.io.common.BytesIO(contents))
    
    if "text" not in df.columns:
        return {"error": "CSV должен содержать колонку 'text'"}

    # Создание папки для загрузок, если не существует
    upload_dir = os.path.join(os.path.dirname(__file__), "../../data/uploads")
    os.makedirs(upload_dir, exist_ok=True)

    # Генерация уникального имени файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(upload_dir, f"{timestamp}_{file.filename}")

    # Сохранение файла на сервере
    save_uploaded_file(contents, save_path)
    logger.info(f"Файл '{file.filename}' загружен и сохранен как '{save_path}'")

    return {"message": f"Файл успешно загружен", "path": save_path}
