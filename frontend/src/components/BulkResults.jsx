import React from "react";
import PredictionCard from "./PredictionCard.jsx";
import CollegeTable from "./CollegeTable.jsx";
import QualificationStatus from "./QualificationStatus.jsx";

export default function BulkResults({ bulk }) {
  return (
    <div className="space-y-5">
      <h2 className="text-lg font-semibold">Bulk Results</h2>

      {bulk.results.map((item) => (
        <div key={item.row} className="rounded-md border border-[#d9e1ea] p-4">
          <p className="mb-3 text-sm font-medium text-[#5d6b7a]">Row {item.row}</p>
          <QualificationStatus prediction={item.prediction} compact />
          <PredictionCard prediction={item.prediction} compact />
          <CollegeTable colleges={item.prediction.colleges} />
        </div>
      ))}

      {bulk.errors.length > 0 && (
        <div className="rounded-md border border-[#f0b8a8] bg-[#fff4ef] p-4 text-sm text-[#8a2f18]">
          {bulk.errors.map((item) => (
            <p key={item.row}>Row {item.row}: {item.error}</p>
          ))}
        </div>
      )}
    </div>
  );
}