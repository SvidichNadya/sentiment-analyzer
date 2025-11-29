// API сервис для работы с backend
const BASE_URL = "http://localhost:8000/api";

/**
 * Загрузка CSV файла на сервер и анализ тональности
 * @param {File} file - CSV файл
 * @returns {Promise<Object>} - JSON с результатом анализа
 */
export async function uploadCSV(file) {
  if (!file) throw new Error("No file provided");

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Ошибка при загрузке файла");
  }

  return await response.json();
}

/**
 * Получение результатов анализа текста
 * @returns {Promise<Object>} - JSON с размеченными данными
 */
export async function getAnalysisResults() {
  const response = await fetch(`${BASE_URL}/prediction`, {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error("Ошибка при получении результатов анализа");
  }

  return await response.json();
}

/**
 * Выполнение поиска текстов по ключевым словам или источникам
 * @param {string} query - поисковый запрос
 * @param {string} source - источник данных (необязательно)
 * @returns {Promise<Array>} - массив найденных текстов
 */
export async function searchTexts(query, source = "") {
  const params = new URLSearchParams();
  if (query) params.append("query", query);
  if (source) params.append("source", source);

  const response = await fetch(`${BASE_URL}/search?${params.toString()}`, {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error("Ошибка при поиске текстов");
  }

  return await response.json();
}

/**
 * Ручная корректировка меток тональности
 * @param {Array} updatedData - массив объектов с обновлёнными label
 * @returns {Promise<Object>} - результат обновления
 */
export async function updateLabels(updatedData) {
  const response = await fetch(`${BASE_URL}/admin/update_labels`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ data: updatedData }),
  });

  if (!response.ok) {
    throw new Error("Ошибка при обновлении меток");
  }

  return await response.json();
}

/**
 * Оценка модели по валидационному CSV
 * @param {File} file - CSV файл с валидационной выборкой
 * @returns {Promise<Object>} - JSON с метрикой macro-F1
 */
export async function evaluateModel(file) {
  if (!file) throw new Error("No validation file provided");

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/validation`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Ошибка при оценке модели");
  }

  return await response.json();
}
