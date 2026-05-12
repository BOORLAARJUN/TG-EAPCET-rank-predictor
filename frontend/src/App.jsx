import React, { useState } from "react";
import { AlertCircle } from "lucide-react";
import { predict, predictBulk } from "./services/api.js";
import PageHeader from "./components/PageHeader.jsx";
import InputPanel from "./components/InputPanel.jsx";
import InfoGrid from "./components/InfoGrid.jsx";
import QualificationGuide from "./components/QualificationGuide.jsx";
import ResultsPanel from "./components/ResultsPanel.jsx";

export default function App() {
  console.log("API URL:", import.meta.env.VITE_API_URL);
  const [prediction, setPrediction] = useState(null);
  const [bulk, setBulk] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handlePredict(values) {
    setLoading(true);
    setError("");
    setBulk(null);
    try {
      const result = await predict(values);
      setPrediction(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleBulk(file) {
    setLoading(true);
    setError("");
    setPrediction(null);
    try {
      const result = await predictBulk(file);
      setBulk(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#f6f8fb] text-[#17202a]">
      <PageHeader loading={loading} />

      <div className="mx-auto w-full max-w-7xl px-4 py-4 sm:px-5 sm:py-6 lg:px-6 lg:py-7">
        <section className="space-y-4 sm:space-y-5">
          <InfoGrid />
          <QualificationGuide />

          {error && (
            <div className="flex items-start gap-3 rounded-md border border-[#f0b8a8] bg-[#fff4ef] p-4 text-[#8a2f18]">
              <AlertCircle size={20} className="mt-0.5 shrink-0" />
              <p className="text-sm leading-6">{error}</p>
            </div>
          )}
        </section>

        <section className="mt-5 grid grid-cols-1 gap-5 lg:mt-6 lg:grid-cols-[minmax(320px,380px)_minmax(0,1fr)] lg:items-start">
          <div className="min-w-0">
            <InputPanel
              loading={loading}
              onPredict={handlePredict}
              onBulkUpload={handleBulk}
            />
          </div>

          <div className="min-w-0">
            <ResultsPanel prediction={prediction} bulk={bulk} />
          </div>
        </section>
      </div>
    </main>
  );
}