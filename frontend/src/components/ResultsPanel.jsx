import React from "react";
import { GraduationCap } from "lucide-react";
import PredictionCard from "./PredictionCard.jsx";
import CollegeTable from "./CollegeTable.jsx";
import QualificationStatus from "./QualificationStatus.jsx";
import BulkResults from "./BulkResults.jsx";

export default function ResultsPanel({ prediction, bulk }) {
  if (prediction) {
    return (
      <section className="min-h-[320px] min-w-0 overflow-hidden rounded-md border border-[#d9e1ea] bg-white p-4 shadow-sm sm:p-5">
        <div className="space-y-5">
          <QualificationStatus prediction={prediction} />
          <PredictionCard prediction={prediction} />
          <div className="min-w-0 overflow-x-auto">
            <CollegeTable colleges={prediction.colleges} />
          </div>
        </div>
      </section>
    );
  }

  if (bulk) {
    return (
      <section className="min-h-[320px] min-w-0 overflow-hidden rounded-md border border-[#d9e1ea] bg-white p-4 shadow-sm sm:p-5">
        <BulkResults bulk={bulk} />
      </section>
    );
  }

  return (
    <section className="min-h-[320px] rounded-md border border-[#d9e1ea] bg-white p-4 shadow-sm sm:p-5">
      <div className="flex min-h-[260px] items-center justify-center text-center">
        <div>
          <GraduationCap className="mx-auto mb-4 text-[#0f766e]" size={42} />
          <h2 className="text-base font-semibold sm:text-lg">Ready for a prediction</h2>
          <p className="mt-2 max-w-sm text-sm leading-6 text-[#5d6b7a]">
            Enter marks or upload a CSV to see qualification status, normalized score,
            predicted rank, rank band, and college shortlist results.
          </p>
        </div>
      </div>
    </section>
  );
}