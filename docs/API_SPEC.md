# API Specification

## Base URL
/api

## Endpoints

### 1. `/api/predict`
- **POST**: Прогноз тональности для текстов
- **Body**: JSON `{ "texts": ["текст1", "текст2"] }`
- **Response**: `{ "predictions": [0, 2] }`

### 2. `/api/validate`
- **POST**: Оценка модели по CSV валидации
- **Body**: multipart/form-data файл CSV
- **Response**: `{ "macro_f1": 0.85, "details": {...} }`

### 3. `/api/upload`
- **POST**: Загрузка CSV файлов
- **Response**: `{ "message": "File uploaded successfully" }`

### 4. `/api/search`
- **GET**: Поиск по словоформам и источникам
- **Query Params**: `?q=слово&src=rureviews`
- **Response**: `{ "results": [...] }`

### 5. `/api/admin`
- **POST/PUT**: Ручная корректировка разметки
- **Body**: `{ "id": 123, "label": 2 }`
- **Response**: `{ "message": "Label updated" }`
