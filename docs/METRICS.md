# Evaluation Metrics

## Macro-F1
- Среднее F1 по всем классам (0, 1, 2)
- Формула: Macro-F1 = 1/N * Σ_i=1^N 2 * (Precision_i * Recall_i) / (Precision_i + Recall_i)

## Precision, Recall
- Precision_i = TP_i / (TP_i + FP_i)
- Recall_i = TP_i / (TP_i + FN_i)

## Usage
- Используется в `/api/validate`
- Отображается в Dashboard фронтенда

