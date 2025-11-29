import React, { useState } from "react";
import { useApi } from "../hooks/useApi.js";

export default function ModelEvaluator() {
  const { evaluateModel, loading, error } = useApi();
  const [validationFile, setValidationFile] = useState(null);
  const [score, setScore] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      setValidationFile(e.target.files[0]);
      setScore(null);
    }
  };

  const handleEvaluate = async () => {
    if (!validationFile) {
      alert("Выберите CSV-файл для оценки модели.");
      return;
    }

    try {
      const result = await evaluateModel(validationFile);
      if (result && result.macroF1 !== undefined) {
        setScore(result.macroF1.toFixed(4));
      } else {
        alert("Ошибка при вычислении метрики.");
      }
    } catch (err) {
      console.error(err);
      alert("Ошибка при оценке модели.");
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-md">
      <h3 className="text-lg font-semibold mb-4">Оценка модели (Macro-F1)</h3>

      <input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        className="mb-4"
      />

      <button
        onClick={handleEvaluate}
        disabled={loading || !validationFile}
        className={`px-4 py-2 rounded-md font-semibold text-white ${
          loading || !validationFile
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-purple-600 hover:bg-purple-700"
        }`}
      >
        {loading ? "Вычисление..." : "Оценить модель"}
      </button>

      {score !== null && (
        <p className="mt-4 text-green-600 font-semibold">
          Macro-F1: {score}
        </p>
      )}

      {error && <p className="mt-2 text-red-500">{error}</p>}
    </div>
  );
}
