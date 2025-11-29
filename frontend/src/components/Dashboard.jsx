import React, { useState, useEffect } from "react";
import FileUploader from "./FileUploader.jsx";
import TextAnalyzer from "./TextAnalyzer.jsx";
import { useApi } from "../hooks/useApi.js";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Регистрация компонентов Chart.js
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function Dashboard() {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [textData, setTextData] = useState([]);
  const { fetchAnalysis, loading, error } = useApi();

  // Загрузка анализа после загрузки файла
  useEffect(() => {
    if (uploadedFile) {
      loadAnalysis();
    }
  }, [uploadedFile]);

  const loadAnalysis = async () => {
    const result = await fetchAnalysis();
    if (result && result.data) {
      setTextData(result.data);
    }
  };

  // Подготовка данных для графика тональности
  const sentimentCounts = textData.reduce(
    (acc, item) => {
      acc[item.label] = (acc[item.label] || 0) + 1;
      return acc;
    },
    {}
  );

  const chartData = {
    labels: ["Отрицательная", "Нейтральная", "Положительная"],
    datasets: [
      {
        label: "Количество отзывов",
        data: [
          sentimentCounts[0] || 0,
          sentimentCounts[1] || 0,
          sentimentCounts[2] || 0,
        ],
        backgroundColor: ["#f87171", "#9ca3af", "#34d399"], // Tailwind цвета
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: "Распределение тональности отзывов" },
    },
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Анализатор тональности отзывов</h1>

      {/* Загрузка CSV */}
      <FileUploader onUpload={(file) => setUploadedFile(file)} />

      {/* График тональности */}
      {textData.length > 0 && (
        <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
          <Bar data={chartData} options={chartOptions} />
        </div>
      )}

      {/* Анализ текста */}
      {uploadedFile && (
        <div className="mt-8">
          <TextAnalyzer uploadedFile={uploadedFile} />
        </div>
      )}

      {/* Статусы */}
      {loading && <p className="mt-4 text-gray-600">Загрузка данных...</p>}
      {error && <p className="mt-4 text-red-500">{error}</p>}
    </div>
  );
}
