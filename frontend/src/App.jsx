import React, { useState } from "react";
import FileUploader from "./components/FileUploader.jsx";
import TextAnalyzer from "./components/TextAnalyzer.jsx";
import Dashboard from "./components/Dashboard.jsx";
import SearchPanel from "./components/SearchPanel.jsx";
import ManualLabelEditor from "./components/ManualLabelEditor.jsx";
import ModelEvaluator from "./components/ModelEvaluator.jsx";

function App() {
  // Загруженные данные и результаты анализа
  const [uploadedData, setUploadedData] = useState([]);
  const [analyzedData, setAnalyzedData] = useState([]);
  const [selectedText, setSelectedText] = useState(null);

  // Статус загрузки/анализа
  const [status, setStatus] = useState("");

  // Функция обработки загрузки CSV
  const handleUpload = async (file) => {
    if (!file) return;
    setStatus("Загрузка и анализ файла...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();

      if (result.success) {
        setUploadedData(result.data);
        setAnalyzedData(result.data);
        setStatus("Файл успешно загружен и проанализирован");
      } else {
        setStatus("Ошибка при обработке файла");
      }
    } catch (err) {
      console.error(err);
      setStatus("Ошибка сервера при загрузке файла");
    }
  };

  // Функция обновления данных после ручной корректировки
  const handleManualUpdate = (updatedData) => {
    setAnalyzedData(updatedData);
  };

  // Функция выбора текста для подробного анализа
  const handleSelectText = (text) => {
    setSelectedText(text);
  };

  return (
    <div className="flex flex-col min-h-screen">
      {/* Upload CSV Section */}
      <section id="upload" className="py-12 px-4 md:px-16 bg-gray-50 flex flex-col items-center">
        <h3 className="text-3xl font-bold text-gray-800 mb-6">Загрузите CSV с отзывами</h3>
        <FileUploader onUpload={handleUpload} />
        {status && <p className="mt-4 text-gray-600">{status}</p>}
      </section>

      {/* Results Section */}
      <section id="results" className="py-12 px-4 md:px-16 bg-white flex flex-col items-center">
        <h3 className="text-3xl font-bold text-gray-800 mb-6">Результаты анализа</h3>
        <TextAnalyzer
          data={analyzedData}
          onSelectText={handleSelectText}
        />
      </section>

      {/* Dashboard Section */}
      <section id="dashboard" className="py-12 px-4 md:px-16 bg-gray-50 flex flex-col items-center">
        <h3 className="text-3xl font-bold text-gray-800 mb-6">Дашборд визуализации</h3>
        <Dashboard data={analyzedData} />
      </section>

      {/* Search / Filtering Section */}
      <section id="search" className="py-12 px-4 md:px-16 bg-white flex flex-col items-center">
        <h3 className="text-3xl font-bold text-gray-800 mb-6">Поиск и фильтрация</h3>
        <SearchPanel
          data={analyzedData}
          onSelectText={handleSelectText}
        />
      </section>

      {/* Manual Label Editing Section */}
      <section id="manual-label" className="py-12 px-4 md:px-16 bg-gray-50 flex flex-col items-center">
        <h3 className="text-3xl font-bold text-gray-800 mb-6">Ручная корректировка разметки</h3>
        <ManualLabelEditor
          data={analyzedData}
          onUpdate={handleManualUpdate}
        />
      </section>

      {/* Model Evaluation Section */}
      <section id="evaluation" className="py-12 px-4 md:px-16 bg-white flex flex-col items-center">
        <h3 className="text-3xl font-bold text-gray-800 mb-6">Оценка модели</h3>
        <ModelEvaluator data={analyzedData} />
      </section>
    </div>
  );
}

export default App;
