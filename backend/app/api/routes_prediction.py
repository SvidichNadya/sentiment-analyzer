# backend/app/api/routes_prediction.py

from fastapi import APIRouter, Depends, UploadFile, File
from typing import List
import pandas as pd
import io

from ..dependencies import get_model_handler, get_tokenizer
from ..ml.dataset import TextDataset
from ..ml.model import ModelHandler
from ..utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/predict", tags=["Prediction"])

# --------------------------------------------------------
# Эндпоинт: предсказание тональности текстов
# --------------------------------------------------------
@router.post("/text")
async def predict_texts(
    texts: List[str],
    model_handler: ModelHandler = Depends(get_model_handler),
    tokenizer = Depends(get_tokenizer)
):
    """
    Предсказывает тональность списка текстов.
    Возвращает список меток: 0 - отрицательная, 1 - нейтральная, 2 - положительная
    """
    dataset = TextDataset(texts=texts, tokenizer=tokenizer)
    dataloader = model_handler.model.device  # Будет заменен на DataLoader
    from torch.utils.data import DataLoader
    dataloader = DataLoader(dataset, batch_size=32, collate_fn=dataset.collate_fn)

    preds = model_handler.predict(dataloader)
    logger.info(f"Предсказание для {len(texts)} текстов выполнено.")
    return {"predictions": preds}

# --------------------------------------------------------
# Эндпоинт: предсказание из CSV файла
# --------------------------------------------------------
@router.post("/file")
async def predict_file(
    file: UploadFile = File(...),
    model_handler: ModelHandler = Depends(get_model_handler),
    tokenizer = Depends(get_tokenizer)
):
    """
    Предсказывает тональность текстов из загруженного CSV-файла.
    Ожидается колонка 'text'.
    """
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    if "text" not in df.columns:
        return {"error": "CSV должен содержать колонку 'text'"}

    texts = df["text"].tolist()
    dataset = TextDataset(texts=texts, tokenizer=tokenizer)
    from torch.utils.data import DataLoader
    dataloader = DataLoader(dataset, batch_size=32, collate_fn=dataset.collate_fn)

    preds = model_handler.predict(dataloader)
    df["predicted_label"] = preds
    logger.info(f"Предсказание из CSV-файла '{file.filename}' выполнено. Пример 5 результатов:\n{df.head()}")
    return {"predictions": df.to_dict(orient="records")}
