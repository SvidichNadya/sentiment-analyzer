# backend/app/core/evaluation.py

from typing import List
import pandas as pd
from sklearn.metrics import f1_score
from ..utils.logger import get_logger

logger = get_logger(__name__)

# --------------------------------------------------------
# Класс Evaluator
# --------------------------------------------------------

class Evaluator:
    """
    Оценка модели классификации по метрике macro-F1.
    """

    def __init__(self):
        logger.info("Evaluator инициализирован")

    # ----------------------------------------------------
    # Расчет macro-F1 для списков предсказаний и истинных меток
    # ----------------------------------------------------
    def compute_macro_f1(self, y_true: List[int], y_pred: List[int]) -> float:
        """
        Вычисляет macro-F1
        """
        if not y_true or not y_pred:
            raise ValueError("y_true и y_pred не должны быть пустыми")

        score = f1_score(y_true, y_pred, average="macro")
        logger.info(f"Вычислен macro-F1: {score:.4f}")
        return score

    # ----------------------------------------------------
    # Расчет macro-F1 по DataFrame с колонками target и pred
    # ----------------------------------------------------
    def compute_from_dataframe(self, df: pd.DataFrame, target_col: str = "label", pred_col: str = "pred") -> float:
        """
        Вычисляет macro-F1 для DataFrame с размеченными данными
        """
        if target_col not in df.columns or pred_col not in df.columns:
            raise ValueError(f"DataFrame должен содержать колонки {target_col} и {pred_col}")

        y_true = df[target_col].tolist()
        y_pred = df[pred_col].tolist()

        return self.compute_macro_f1(y_true, y_pred)

# --------------------------------------------------------
# Удобная функция для быстрого вычисления macro-F1
# --------------------------------------------------------
def macro_f1_score(y_true: List[int], y_pred: List[int]) -> float:
    evaluator = Evaluator()
    return evaluator.compute_macro_f1(y_true, y_pred)
