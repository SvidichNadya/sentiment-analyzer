# Deployment Guide

## Docker Compose
cd deployment
docker-compose up --build
- Backend: `http://localhost:8000/api`
- Frontend: `http://localhost:3000`

## Cloud Deployment

### Render
- Использовать `render.yaml`
- Настроить backend и frontend как веб-сервисы
- Переменные окружения: `ENV=production`, `PORT=8000`, `REACT_APP_API_URL=https://backend-url/api`

### Fly.io
- Использовать `fly.toml`
- `fly deploy` для backend и frontend
- Fly автоматически выдаст TLS сертификаты

### Vercel
- Использовать `vercel.json`
- Настроить переменную окружения `REACT_APP_API_URL`
- Прокси `/api/*` на backend
