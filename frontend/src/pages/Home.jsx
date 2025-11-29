import React, { useState } from "react";
import FileUploader from "../components/FileUploader.jsx";
import TextAnalyzer from "../components/TextAnalyzer.jsx";
import Dashboard from "../components/Dashboard.jsx";
import SearchPanel from "../components/SearchPanel.jsx";
import ManualLabelEditor from "../components/ManualLabelEditor.jsx";
import ModelEvaluator from "../components/ModelEvaluator.jsx";

export default function Home() {
  const [analyzedTexts, setAnalyzedTexts] = useState([]);
  const [searchResults, setSearchResults] = useState([]);

  // После анализа текста обновляем список текстов
  const handleAnalysisComplete = (results) => {
    setAnalyzedTexts(results);
    setSearchResults(results);
  };

  // После поиска обновляем отображаемые результаты
  const handleSearchResults = (results) => {
    setSearchResults(results);
  };

  // После ручного редактирования обновляем тексты
  const handleManualUpdate = (updatedTexts) => {
    setAnalyzedTexts(updatedTexts);
    setSearchResults(updatedTexts);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Анализатор тональности отзывов
      </h1>

      {/* Шаг 1: Загрузка файлов */}
      <FileUploader onUploadComplete={handleAnalysisComplete} />

      {/* Шаг 2: Анализ текста */}
      <TextAnalyzer texts={analyzedTexts} onAnalysisComplete={handleAnalysisComplete} />

      <div className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Панель поиска и фильтры */}
        <SearchPanel onSearchResults={handleSearchResults} />

        {/* Ручная корректировка разметки */}
        <ManualLabelEditor texts={searchResults} onUpdate={handleManualUpdate} />
      </div>

      <div className="mt-6">
        {/* Дашборд с визуализациями */}
        <Dashboard texts={searchResults} />
      </div>

      <div className="mt-6 max-w-md mx-auto">
        {/* Оценка модели */}
        <ModelEvaluator />
      </div>
    </div>
  );
}
