import React, { useState, useEffect } from "react";
import { useApi } from "../hooks/useApi.js";

export default function SearchPanel({ onSearchResults }) {
  const { searchTexts, loading, error } = useApi();
  const [query, setQuery] = useState("");
  const [sourceFilter, setSourceFilter] = useState("all");
  const [sentimentFilter, setSentimentFilter] = useState("all");
  const [sources, setSources] = useState([]);

  // Получение доступных источников при загрузке
  useEffect(() => {
    async function fetchSources() {
      const result = await searchTexts({ getSourcesOnly: true });
      if (result && result.sources) {
        setSources(result.sources);
      }
    }
    fetchSources();
  }, []);

  const handleSearch = async () => {
    const params = {
      query,
      source: sourceFilter === "all" ? null : sourceFilter,
      sentiment:
        sentimentFilter === "all" ? null : Number(sentimentFilter),
    };
    const results = await searchTexts(params);
    if (results && results.data) {
      onSearchResults(results.data);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-xl mb-6">
      <h3 className="text-lg font-semibold mb-4">Поиск и фильтрация текстов</h3>

      <div className="flex flex-col gap-4">
        <input
          type="text"
          placeholder="Введите ключевое слово..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="px-3 py-2 border rounded-md"
        />

        <div className="flex gap-4">
          <select
            value={sourceFilter}
            onChange={(e) => setSourceFilter(e.target.value)}
            className="px-3 py-2 border rounded-md flex-1"
          >
            <option value="all">Все источники</option>
            {sources.map((src) => (
              <option key={src} value={src}>
                {src}
              </option>
            ))}
          </select>

          <select
            value={sentimentFilter}
            onChange={(e) => setSentimentFilter(e.target.value)}
            className="px-3 py-2 border rounded-md flex-1"
          >
            <option value="all">Все тональности</option>
            <option value="0">Отрицательная</option>
            <option value="1">Нейтральная</option>
            <option value="2">Положительная</option>
          </select>
        </div>

        <button
          onClick={handleSearch}
          disabled={loading}
          className={`px-4 py-2 rounded-md font-semibold text-white ${
            loading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {loading ? "Поиск..." : "Применить фильтры"}
        </button>

        {error && <p className="text-red-500 mt-2">{error}</p>}
      </div>
    </div>
  );
}
