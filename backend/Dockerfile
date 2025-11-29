# -----------------------------------------------------------------
# Dockerfile для backend платформы анализа тональности
# -----------------------------------------------------------------

# 1️⃣ Базовый образ Python
FROM python:3.11-slim

# 2️⃣ Обновление пакетов и установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 3️⃣ Установка рабочей директории
WORKDIR /app

# 4️⃣ Копирование и установка Python зависимостей
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Копирование исходного кода backend
COPY ./app ./app
COPY ./data ./app/data
COPY ./models ./app/models
COPY ./start.sh ./start.sh

# 6️⃣ Создание папки для загрузки файлов через API
RUN mkdir -p /app/app/data/uploads

# 7️⃣ Экспонирование порта FastAPI
EXPOSE 8000

# 8️⃣ Задаем права на скрипт запуска
RUN chmod +x ./start.sh

# 9️⃣ Команда по умолчанию
CMD ["./start.sh"]
