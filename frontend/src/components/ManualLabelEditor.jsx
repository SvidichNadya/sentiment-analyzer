import React, { useState, useEffect } from "react";
import { useApi } from "../hooks/useApi.js";

const labelOptions = [
  { value: 0, label: "Отрицательная" },
  { value: 1, label: "Нейтральная" },
  { value: 2, label: "Положительная" },
];

export default function ManualLabelEditor({ texts, onUpdate }) {
  const { updateLabel, loading, error } = useApi();
  const [editableTexts, setEditableTexts] = useState([]);

  useEffect(() => {
    if (texts) {
      setEditableTexts(texts.map((item) => ({ ...item })));
    }
  }, [texts]);

  const handleChange = (index, newLabel) => {
    const updated = [...editableTexts];
    updated[index].label = Number(newLabel);
    setEditableTexts(updated);
  };

  const handleSave = async () => {
    try {
      for (let item of editableTexts) {
        await updateLabel(item.id, item.label); // предполагаем уникальный id у каждого текста
      }
      onUpdate(editableTexts);
      alert("Разметка успешно сохранена!");
    } catch (err) {
      console.error(err);
      alert("Ошибка при сохранении разметки.");
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md w-full overflow-x-auto">
      <h3 className="text-lg font-semibold mb-4">Ручная корректировка разметки</h3>

      {editableTexts.length === 0 ? (
        <p>Нет данных для редактирования.</p>
      ) : (
        <table className="min-w-full border border-gray-300">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-4 py-2 border">Текст</th>
              <th className="px-4 py-2 border">Тональность</th>
              <th className="px-4 py-2 border">Источник</th>
            </tr>
          </thead>
          <tbody>
            {editableTexts.map((item, index) => (
              <tr key={item.id || index}>
                <td className="px-4 py-2 border">{item.text}</td>
                <td className="px-4 py-2 border">
                  <select
                    value={item.label}
                    onChange={(e) => handleChange(index, e.target.value)}
                    className="px-2 py-1 border rounded-md"
                  >
                    {labelOptions.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </td>
                <td className="px-4 py-2 border">{item.src}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <button
        onClick={handleSave}
        disabled={loading || editableTexts.length === 0}
        className={`mt-4 px-4 py-2 rounded-md font-semibold text-white ${
          loading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-green-600 hover:bg-green-700"
        }`}
      >
        {loading ? "Сохранение..." : "Сохранить изменения"}
      </button>

      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  );
}
