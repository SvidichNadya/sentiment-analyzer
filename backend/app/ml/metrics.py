# backend/app/ml/metrics.py

from sklearn.metrics import precision_score, recall_score, f1_score
from typing import List, Dict
from ..utils.logger import get_logger

logger = get_logger(__name__)

# --------------------------------------------------------
# Метрики для обучения модели
# --------------------------------------------------------

def precision(y_true: List[int], y_pred: List[int], average: str = "macro") -> float:
    """
    Вычисляет точность (Precision)
    """
    score = precision_score(y_true, y_pred, average=average)
    logger.info(f"Precision ({average}): {score:.4f}")
    return score

def recall(y_true: List[int], y_pred: List[int], average: str = "macro") -> float:
    """
    Вычисляет полноту (Recall)
    """
    score = recall_score(y_true, y_pred, average=average)
    logger.info(f"Recall ({average}): {score:.4f}")
    return score

def f1(y_true: List[int], y_pred: List[int], average: str = "macro") -> float:
    """
    Вычисляет F1-меру
    """
    score = f1_score(y_true, y_pred, average=average)
    logger.info(f"F1 ({average}): {score:.4f}")
    return score

# --------------------------------------------------------
# Метрики для батча во время тренировки
# --------------------------------------------------------

def compute_metrics(preds: List[int], labels: List[int]) -> Dict[str, float]:
    """
    Вычисляет precision, recall и F1 для батча
    """
    precision_score_val = precision(labels, preds)
    recall_score_val = recall(labels, preds)
    f1_score_val = f1(labels, preds)
    return {
        "precision": precision_score_val,
        "recall": recall_score_val,
        "f1": f1_score_val
    }
