# Installation Guide

## Backend
1. Установить Python 3.11
2. Создать виртуальное окружение
python -m venv venv
source venv/bin/activate
3. Установить зависимости:
pip install -r backend/requirements.txt
4. Запустить локально:
cd backend
uvicorn app.main:app --reload --port 8000

## Frontend
1. Установить Node.js 20+
2. Установить зависимости:
npm install
3. Запустить локально:
npm run dev
4. Веб-приложение доступно на `http://localhost:3000`
