import React, { useEffect, useState } from "react";
import { useApi } from "../hooks/useApi.js";

const labelColors = {
  0: "bg-red-200",    // Отрицательная
  1: "bg-gray-200",   // Нейтральная
  2: "bg-green-200",  // Положительная
};

export default function TextAnalyzer({ uploadedFile }) {
  const { fetchAnalysis, searchTexts, loading, error } = useApi();
  const [texts, setTexts] = useState([]);
  const [filter, setFilter] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");

  // Получение результатов анализа после загрузки файла
  useEffect(() => {
    if (uploadedFile) {
      loadAnalysis();
    }
  }, [uploadedFile]);

  const loadAnalysis = async () => {
    const result = await fetchAnalysis();
    if (result) {
      setTexts(result.data || []);
    }
  };

  // Фильтрация и поиск
  const filteredTexts = texts.filter((item) => {
    const matchesFilter =
      filter === "all" ? true : Number(item.label) === Number(filter);
    const matchesSearch = item.text
      .toLowerCase()
      .includes(searchQuery.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  return (
    <div className="w-full p-4 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Результаты анализа</h2>

      <div className="flex flex-wrap gap-4 mb-4">
        <input
          type="text"
          placeholder="Поиск по тексту..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="px-3 py-2 border rounded-md w-64"
        />
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-3 py-2 border rounded-md"
        >
          <option value="all">Все</option>
          <option value="0">Отрицательные</option>
          <option value="1">Нейтральные</option>
          <option value="2">Положительные</option>
        </select>
      </div>

      {loading ? (
        <p>Загрузка данных...</p>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : filteredTexts.length === 0 ? (
        <p>Нет данных для отображения.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full border border-gray-300">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 border">Текст</th>
                <th className="px-4 py-2 border">Тональность</th>
                <th className="px-4 py-2 border">Источник</th>
              </tr>
            </thead>
            <tbody>
              {filteredTexts.map((item, index) => (
                <tr key={index} className={labelColors[item.label]}>
                  <td className="px-4 py-2 border">{item.text}</td>
                  <td className="px-4 py-2 border">
                    {item.label === 0
                      ? "Отрицательная"
                      : item.label === 1
                      ? "Нейтральная"
                      : "Положительная"}
                  </td>
                  <td className="px-4 py-2 border">{item.src}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
