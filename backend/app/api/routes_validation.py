# backend/app/api/routes_validation.py

from fastapi import APIRouter, UploadFile, File, Depends
import pandas as pd
import io
from torch.utils.data import DataLoader

from ..dependencies import get_model_handler, get_tokenizer
from ..ml.dataset import TextDataset
from ..ml.model import ModelHandler
from ..ml.metrics import compute_metrics
from ..utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/validate", tags=["Validation"])

# --------------------------------------------------------
# Эндпоинт: валидация модели через CSV
# --------------------------------------------------------
@router.post("/file")
async def validate_model(
    file: UploadFile = File(...),
    model_handler: ModelHandler = Depends(get_model_handler),
    tokenizer = Depends(get_tokenizer)
):
    """
    Валидирует модель по CSV-файлу с колонками:
    'text' — текст, 'label' — истинная метка
    Возвращает метрики macro-F1, precision, recall
    """
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    if "text" not in df.columns or "label" not in df.columns:
        return {"error": "CSV должен содержать колонки 'text' и 'label'"}

    texts = df["text"].tolist()
    labels = df["label"].tolist()

    dataset = TextDataset(texts=texts, labels=labels, tokenizer=tokenizer)
    dataloader = DataLoader(dataset, batch_size=32, collate_fn=dataset.collate_fn)

    preds = model_handler.predict(dataloader)
    metrics = compute_metrics(preds, labels)
    logger.info(f"Валидация CSV '{file.filename}' завершена. Метрики: {metrics}")

    return {"metrics": metrics}
