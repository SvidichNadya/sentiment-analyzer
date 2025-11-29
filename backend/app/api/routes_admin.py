# backend/app/api/routes_admin.py

from fastapi import APIRouter, HTTPException
from typing import List
import os
import pandas as pd

from ..utils.csv_tools import save_csv, load_csv
from ..utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/admin", tags=["Admin"])

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "../../data/uploads")
LABELED_DIR = os.path.join(os.path.dirname(__file__), "../../data/labeled")
os.makedirs(LABELED_DIR, exist_ok=True)

# --------------------------------------------------------
# Получение списка файлов для ручной разметки
# --------------------------------------------------------
@router.get("/files")
def list_uploaded_files():
    """
    Возвращает список загруженных файлов для ручной разметки
    """
    files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".csv")]
    return {"files": files}

# --------------------------------------------------------
# Получение содержимого файла для редактирования
# --------------------------------------------------------
@router.get("/file")
def get_file(file_name: str):
    """
    Возвращает содержимое CSV-файла для ручной корректировки разметки
    """
    path = os.path.join(UPLOAD_DIR, file_name)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    df = load_csv(path)
    return {"data": df.to_dict(orient="records")}

# --------------------------------------------------------
# Сохранение корректировки вручную
# --------------------------------------------------------
@router.post("/file/save")
def save_labeled_file(file_name: str, labeled_data: List[dict]):
    """
    Сохраняет вручную размеченные данные в отдельную папку LABELED_DIR
    """
    df = pd.DataFrame(labeled_data)
    save_path = os.path.join(LABELED_DIR, file_name)
    save_csv(df, save_path)
    logger.info(f"Файл '{file_name}' сохранен в '{save_path}' после ручной корректировки.")
    return {"message": f"Файл успешно сохранен", "path": save_path}
