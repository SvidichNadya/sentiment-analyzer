# backend/app/api/routes_search.py

from fastapi import APIRouter, Query
from typing import List, Optional
import os
import pandas as pd

from ..core.search_engine import SearchEngine
from ..utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/search", tags=["Search"])

# --------------------------------------------------------
# Эндпоинт: поиск текстов по ключевым словам
# --------------------------------------------------------
@router.get("/texts")
def search_texts(
    query: str = Query(..., description="Ключевое слово или словоформа для поиска"),
    sources: Optional[List[str]] = Query(None, description="Список источников для фильтрации")
):
    """
    Выполняет поиск текстов по ключевым словам и, опционально, по источникам.
    """
    data_dir = os.path.join(os.path.dirname(__file__), "../../data")
    train_file = os.path.join(data_dir, "train.csv")

    df = pd.read_csv(train_file)

    # Фильтрация по источникам, если задано
    if sources:
        df = df[df["src"].isin(sources)]

    search_engine = SearchEngine(df)
    results = search_engine.search(query)

    logger.info(f"Поиск по слову '{query}' выполнен. Найдено {len(results)} результатов.")
    return {"query": query, "sources": sources, "results": results}
