# System Overview

## Общая архитектура платформы

Платформа разделена на три ключевых слоя:

1. **Frontend (React/Vite)**
   - Страницы: Home, Results, Validation, Admin
   - Компоненты: FileUploader, TextAnalyzer, Dashboard, SearchPanel, ManualLabelEditor, ModelEvaluator
   - Взаимодействует с backend через REST API (`/api/*`)

2. **Backend (FastAPI + PyTorch)**
   - Модули:
     - `core` — обработка текста, нормализация, поиск, метрики
     - `ml` — обучение, токенизация, Dataset, inference, метрики
     - `api` — роуты для предсказаний, валидации, загрузки файлов, поиска и администрирования
     - `utils` — файловые операции, логирование, CSV-генерация
   - Поддержка загрузки CSV, ручной корректировки разметки, оценки по macro-F1

3. **Deployment**
   - Docker Compose для локального запуска
   - Nginx для фронтенда с проксированием API
   - Поддержка облачного деплоя (Render, Fly.io, Vercel)

## Поток данных

User CSV → Backend API → NLP Preprocessing → Model Inference → CSV + Dashboard Visualization → Frontend


- Backend принимает CSV, нормализует текст, прогоняет через модель, возвращает размеченный CSV.
- Frontend визуализирует результаты и позволяет ручную корректировку.

## Хранение данных

- `data/` — исходные CSV (train, test)
- `models/` — обученные модели и токенизатор
- Docker Volumes для сохранения данных между перезапусками
