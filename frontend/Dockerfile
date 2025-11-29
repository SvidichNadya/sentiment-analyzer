# ----------------- STAGE 1: BUILD -----------------
FROM node:20-alpine AS builder

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json (если есть)
COPY package.json package-lock.json* ./

# Устанавливаем зависимости
RUN npm install --frozen-lockfile

# Копируем исходный код фронтенда
COPY . .

# Сборка проекта
RUN npm run build

# ----------------- STAGE 2: SERVE -----------------
FROM nginx:alpine

# Копируем собранные файлы из builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Копируем кастомную конфигурацию nginx (опционально)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Открываем порт
EXPOSE 80

# Команда запуска nginx
CMD ["nginx", "-g", "daemon off;"]
