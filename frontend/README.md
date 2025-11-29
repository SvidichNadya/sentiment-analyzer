# Sentiment Analyzer Frontend

## Описание
Веб-интерфейс для платформы анализа тональности русскоязычных текстов.  
Позволяет пользователям загружать CSV с отзывами, просматривать результаты классификации, фильтровать и искать тексты, редактировать разметку вручную и визуализировать статистику.

## Структура проекта
- `public/` — статические файлы (index.html, favicon и т.д.)
- `src/`
  - `components/` — переиспользуемые UI-компоненты (FileUploader, TextAnalyzer, Dashboard, SearchPanel, ManualLabelEditor, ModelEvaluator)
  - `pages/` — страницы приложения (Home, Results, Validation, Admin)
  - `services/` — API-клиент для общения с backend
  - `hooks/` — кастомные React hooks (useApi)
  - `styles/` — глобальные и компонентные CSS
- `package.json` — зависимости и скрипты проекта
- `vite.config.js` — конфигурация сборщика Vite
- `Dockerfile` — контейнеризация frontend

## Требования
- Node.js 20+
- npm или yarn

## Локальный запуск
cd frontend
npm install
npm run dev

## Скрипты
npm run dev — запуск в режиме разработки с hot reload
npm run build — сборка продакшн версии
npm run preview — локальный просмотр собранного приложения
npm run test — запуск тестов

## Деплой
Проект готов к деплою на:
Vercel (статический фронт)
Docker контейнер (с nginx или standalone)

## Ссылки
API взаимодействия: services/api.js
Основные компоненты: components/
Страницы приложения: pages/