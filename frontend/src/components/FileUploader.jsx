import React, { useState } from "react";
import { useApi } from "../hooks/useApi.js";

export default function FileUploader({ onUpload }) {
  const { uploadCSV, loading, error } = useApi();
  const [selectedFile, setSelectedFile] = useState(null);

  // Обработчик выбора файла
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "text/csv") {
      setSelectedFile(file);
    } else {
      alert("Пожалуйста, выберите файл CSV");
      setSelectedFile(null);
    }
  };

  // Обработчик отправки файла
  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      const result = await uploadCSV(selectedFile);
      if (result) {
        onUpload(selectedFile); // уведомляем родителя о загрузке
      }
    } catch (err) {
      console.error("Ошибка загрузки:", err);
    }
  };

  return (
    <div className="w-full max-w-lg flex flex-col items-center bg-white p-6 rounded-lg shadow-md">
      <input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        className="mb-4"
      />
      {selectedFile && (
        <p className="text-gray-700 mb-4">Выбран файл: {selectedFile.name}</p>
      )}
      <button
        onClick={handleUpload}
        disabled={!selectedFile || loading}
        className={`px-6 py-2 rounded-md font-semibold text-white ${
          selectedFile
            ? "bg-blue-600 hover:bg-blue-700"
            : "bg-gray-400 cursor-not-allowed"
        }`}
      >
        {loading ? "Загрузка..." : "Загрузить и проанализировать"}
      </button>
      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  );
}
