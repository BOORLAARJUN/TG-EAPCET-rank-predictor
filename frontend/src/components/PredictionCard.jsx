import React from "react";

const NORMALIZATION_DISCLAIMER =
  "This is an unofficial estimate based on TG EAPCET 2026 engineering shift difficulty reports and historical-style adjustment. It is not the official TG EAPCET normalization formula.";

export default function PredictionCard({ prediction, compact = false }) {
  const rawMarks = prediction.raw_predicted_marks ?? prediction.raw_score ?? prediction.normalized_score;
  const rawRank = prediction.raw_predicted_rank ?? prediction.predicted_rank;
  const rawBand = prediction.raw_rank_band ?? prediction.rank_band;
  const estimated = prediction.estimated_normalization;
  const estimatedBand = prediction.estimated_normalized_rank_band;

  return (
    <div className="space-y-4">
      <section className="rounded-md border border-[#d9e1ea] bg-white p-4">
        <h2 className="text-base font-semibold text-[#17202a]">Raw Prediction</h2>
        <div className={`mt-3 grid gap-3 ${compact ? "grid-cols-2 md:grid-cols-4" : "grid-cols-1 md:grid-cols-4"}`}>
          <Metric label="Raw predicted marks" value={formatNumber(rawMarks)} />
          <Metric label="Raw predicted rank" value={formatRank(rawRank)} />
          <Metric label="Raw rank band" value={`${formatRank(rawBand.min)} - ${formatRank(rawBand.max)}`} />
          <Metric label="Model" value={prediction.model_version} />
        </div>
      </section>

      {estimated && (
        <section className="rounded-md border border-[#d9e1ea] bg-[#fbfcfe] p-4">
          <h2 className="text-base font-semibold text-[#17202a]">Estimated Normalized Prediction</h2>
          <div className={`mt-3 grid gap-3 ${compact ? "grid-cols-2 md:grid-cols-4" : "grid-cols-1 md:grid-cols-3"}`}>
            <Metric label="Exam shift" value={estimated.shift_label} />
            <Metric label="Difficulty label" value={formatDifficulty(estimated.difficulty)} />
            <Metric label="Adjustment range" value={`${formatSigned(estimated.adjustment_min)} to ${formatSigned(estimated.adjustment_max)}`} />
            <Metric label="Estimated marks range" value={`${formatNumber(estimated.adjusted_marks_min)} - ${formatNumber(estimated.adjusted_marks_max)}`} />
            <Metric label="Likely normalized marks" value={formatNumber(estimated.adjusted_marks_mid)} />
            <Metric label="Estimated normalized rank" value={formatRank(prediction.estimated_normalized_rank)} />
            {estimatedBand && (
              <Metric
                label="Estimated rank range"
                value={`Best ${formatRank(estimatedBand.best_case)} | Likely ${formatRank(estimatedBand.likely)} | Worst ${formatRank(estimatedBand.worst_case)}`}
              />
            )}
          </div>
          <p className="mt-3 rounded-md border border-[#f0d9a8] bg-[#fff9eb] p-3 text-xs leading-5 text-[#74541a]">
            {NORMALIZATION_DISCLAIMER}
          </p>
        </section>
      )}
    </div>
  );
}

function formatNumber(value) {
  return Number(value).toLocaleString(undefined, { maximumFractionDigits: 2 });
}

function formatRank(value) {
  return Number(value).toLocaleString();
}

function formatSigned(value) {
  const number = Number(value);
  return `${number > 0 ? "+" : ""}${formatNumber(number)}`;
}

function formatDifficulty(value) {
  return String(value).replaceAll("_", " ");
}

function Metric({ label, value }) {
  return (
    <div className="rounded-md border border-[#d9e1ea] bg-[#f9fbfd] p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-[#5d6b7a]">{label}</p>
      <p className="mt-2 text-xl font-semibold text-[#17202a]">{value}</p>
    </div>
  );
}
