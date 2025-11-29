# Sentiment Analyzer Backend

## Описание
Серверная часть платформы анализа тональности русскоязычных текстов.  
Включает:
- REST API (FastAPI) для взаимодействия с фронтендом
- Модель машинного обучения (PyTorch) для классификации отзывов
- NLP пайплайн для предобработки текста (токенизация, лемматизация, нормализация)
- Генерацию CSV и визуализации результатов
- Поддержку ручной корректировки разметки и оценки модели по macro-F1

## Структура проекта
- `app/` — основная логика backend
  - `api/` — маршруты API
  - `core/` — NLP-пайплайн, поиск, оценка модели
  - `ml/` — модель, обучение, токенизация, метрики
  - `utils/` — вспомогательные функции (логирование, обработка файлов, CSV)
  - `__init__.py`, `main.py`, `config.py`, `dependencies.py`
- `models/` — сохраненные модели и конфигурации (trained_model.pt, vocab.json, config.json)
- `data/` — исходные CSV-файлы (train.csv, test.csv, sample_submission.csv)
- `tests/` — unit и интеграционные тесты
- `requirements.txt` — зависимости Python
- `Dockerfile`, `start.sh` — запуск и контейнеризация

## Требования
- Python 3.11+
- PyTorch, Transformers, FastAPI, Pandas, Numpy, Scikit-learn
- Docker (опционально для локального деплоя)

## Локальный запуск
cd backend
pip install -r requirements.txt
bash start.sh

## Тестирование
Unit-тесты: pytest tests/
Проверка предобработки: tests/test_preprocess.py
Проверка модели: tests/test_model.py
End-to-End тесты: tests/test_end_to_end.py

## Деплой
Fly.io (backend)
Docker-compose (локально)
Взаимодействие с frontend через REST API

## Ссылки
Основные маршруты: api/
NLP пайплайн: core/
Обучение и инференс модели: ml/
Вспомогательные функции: utils/