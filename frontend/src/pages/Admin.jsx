import React, { useState } from "react";
import ManualLabelEditor from "../components/ManualLabelEditor.jsx";

export default function Admin() {
  const [texts, setTexts] = useState([]);

  // Обновление текстов после ручной корректировки
  const handleUpdate = (updatedTexts) => {
    setTexts(updatedTexts);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Панель администратора
      </h1>

      <p className="mb-6 text-center text-gray-700 max-w-xl mx-auto">
        Здесь вы можете вручную корректировать разметку тональности текстов, 
        добавлять новые комментарии или проверять автоматически классифицированные отзывы.
      </p>

      <div className="max-w-4xl mx-auto">
        <ManualLabelEditor texts={texts} onUpdate={handleUpdate} />
      </div>
    </div>
  );
}
