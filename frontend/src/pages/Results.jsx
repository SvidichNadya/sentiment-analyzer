import React from "react";
import { saveAs } from "file-saver";
import Dashboard from "../components/Dashboard.jsx";

export default function Results({ texts }) {
  // Функция экспорта CSV
  const handleExportCSV = () => {
    if (!texts || texts.length === 0) {
      alert("Нет данных для экспорта.");
      return;
    }

    const header = ["text", "label", "src"];
    const csvRows = [
      header.join(","),
      ...texts.map((item) =>
        [item.text, item.label, item.src]
          .map((val) => `"${val.toString().replace(/"/g, '""')}"`)
          .join(",")
      ),
    ];

    const blob = new Blob([csvRows.join("\n")], { type: "text/csv;charset=utf-8;" });
    saveAs(blob, "analyzed_texts.csv");
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">Результаты анализа</h1>

      <div className="flex justify-end mb-4">
        <button
          onClick={handleExportCSV}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-semibold"
        >
          Экспорт CSV
        </button>
      </div>

      {texts && texts.length > 0 ? (
        <Dashboard texts={texts} />
      ) : (
        <p className="text-center text-gray-600">Нет данных для отображения.</p>
      )}
    </div>
  );
}
