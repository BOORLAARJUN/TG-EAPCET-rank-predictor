import React from "react";

export default function PredictionCard({ prediction, compact = false }) {
  return (
    <div className={`grid gap-3 ${compact ? "grid-cols-2 md:grid-cols-4" : "grid-cols-1 md:grid-cols-4"}`}>
      <Metric label="Normalized Score" value={prediction.normalized_score} />
      <Metric label="Predicted Rank" value={prediction.predicted_rank.toLocaleString()} />
      <Metric label="Rank Band" value={`${prediction.rank_band.min.toLocaleString()} - ${prediction.rank_band.max.toLocaleString()}`} />
      <Metric label="Model" value={prediction.model_version} />
    </div>
  );
}

function Metric({ label, value }) {
  return (
    <div className="rounded-md border border-[#d9e1ea] bg-[#f9fbfd] p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-[#5d6b7a]">{label}</p>
      <p className="mt-2 text-xl font-semibold text-[#17202a]">{value}</p>
    </div>
  );
}
