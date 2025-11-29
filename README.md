# Sentiment Analyzer Platform

## Описание
Проект представляет собой платформу для анализа тональности русскоязычных текстов.  
Модель классифицирует отзывы по трём категориям: отрицательная, нейтральная, положительная.  
Реализован полный стек: backend (FastAPI + PyTorch), frontend (React + Vite), деплой (Docker, Fly.io, Vercel).

## Функционал
- Загрузка CSV с отзывами
- Автоматическая нормализация текста (токенизация, лемматизация)
- Классификация тональности
- Экспорт размеченных данных в CSV
- Визуализация результатов
- Поиск и фильтрация по текстам и источникам
- Ручная корректировка разметки
- Оценка модели по macro-F1 через валидационную выборку

## Архитектура
- `backend/` — серверная часть, обучение модели, API
- `frontend/` — веб-интерфейс с компонентами для загрузки, анализа, дашбордов
- `deployment/` — конфигурации Docker, nginx, Fly.io, Vercel
- `docs/` — документация, метрики, пайплайны, инструкции
- `.github/` — CI/CD workflows

## Требования
- Python 3.11+
- Node.js 20+
- PyTorch, Transformers, FastAPI, Pandas, Numpy, Scikit-learn
- React 18, Vite
- Docker (для локального деплоя)

## Локальный запуск

### Backend
cd backend
pip install -r requirements.txt
bash start.sh

### Frontend
cd frontend
npm install
npm run dev

### Контейнеризация
docker-compose up --build

### CI/CD
Backend: GitHub Actions + Fly.io
Frontend: GitHub Actions + Vercel
Unit-тесты и интеграционные тесты через GitHub Actions

### Ссылки
Документация API
Системный обзор
Пайплайн NLP
[Метрики и обучение](docs/METRICS.md, docs/TRAINING_NOTEBOOK.ipynb)