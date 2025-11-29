import React from "react";
import ModelEvaluator from "../components/ModelEvaluator.jsx";

export default function Validation() {
  return (
    <div className="min-h-screen bg-gray-100 p-6 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Валидация модели
      </h1>

      <p className="mb-6 text-center text-gray-700 max-w-xl">
        На этой странице вы можете загрузить CSV-файл с размеченной валидационной выборкой
        и оценить качество модели по метрике Macro-F1. Результат поможет понять,
        насколько корректно модель классифицирует тексты по эмоциональной тональности.
      </p>

      <div className="w-full max-w-md">
        <ModelEvaluator />
      </div>
    </div>
  );
}
