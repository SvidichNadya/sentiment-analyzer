import { useState } from "react";
import * as api from "../services/api.js";

/**
 * Кастомный React-хук для работы с backend API
 * Обрабатывает состояние загрузки, ошибки и данные
 */
export function useApi() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  // Загрузка и анализ CSV файла
  const uploadCSV = async (file) => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.uploadCSV(file);
      setData(result.data);
      return result;
    } catch (err) {
      console.error(err);
      setError(err.message || "Ошибка при загрузке файла");
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Получение результатов анализа
  const fetchAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.getAnalysisResults();
      setData(result.data);
      return result;
    } catch (err) {
      console.error(err);
      setError(err.message || "Ошибка при получении результатов анализа");
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Поиск текстов по запросу и источнику
  const searchTexts = async (query, source) => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.searchTexts(query, source);
      setData(result);
      return result;
    } catch (err) {
      console.error(err);
      setError(err.message || "Ошибка при поиске текстов");
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Ручная корректировка меток
  const updateLabels = async (updatedData) => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.updateLabels(updatedData);
      setData(result.data);
      return result;
    } catch (err) {
      console.error(err);
      setError(err.message || "Ошибка при обновлении меток");
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Оценка модели по CSV валидации
  const evaluateModel = async (file) => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.evaluateModel(file);
      return result;
    } catch (err) {
      console.error(err);
      setError(err.message || "Ошибка при оценке модели");
      return null;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    data,
    uploadCSV,
    fetchAnalysis,
    searchTexts,
    updateLabels,
    evaluateModel,
  };
}
