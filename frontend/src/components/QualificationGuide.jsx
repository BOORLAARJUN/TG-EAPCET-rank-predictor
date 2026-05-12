import React from "react";
import { Info, ShieldCheck } from "lucide-react";

export default function QualificationGuide() {
  return (
    <section className="rounded-md border border-[#cfe1ef] bg-[#f7fbff] p-4 sm:p-5">
      <div className="mb-3 flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-[#245b86]">
        <ShieldCheck size={16} />
        EAMCET Qualification Marks
      </div>

      <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
        <div className="rounded-md border border-[#d9e1ea] bg-white p-4">
          <h3 className="text-sm font-semibold text-[#17202a]">OC / BC / OBC categories</h3>
          <p className="mt-2 text-sm leading-6 text-[#5d6b7a]">
            Students generally need at least <span className="font-semibold text-[#17202a]">40 out of 160</span>,
            which is <span className="font-semibold text-[#17202a]">25%</span>, to qualify.
          </p>
        </div>

        <div className="rounded-md border border-[#d9e1ea] bg-white p-4">
          <h3 className="text-sm font-semibold text-[#17202a]">SC / ST categories</h3>
          <p className="mt-2 text-sm leading-6 text-[#5d6b7a]">
            There is <span className="font-semibold text-[#17202a]">no minimum qualifying marks rule</span>
            prescribed for SC and ST candidates.
          </p>
        </div>
      </div>

      <div className="mt-4 rounded-md border border-[#e6edf5] bg-white p-4">
        <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-[#245b86]">
          <Info size={16} />
          Important
        </div>
        <ul className="space-y-2 text-sm leading-6 text-[#5d6b7a]">
          <li>Qualifying the exam does not guarantee a seat.</li>
          <li>Admission still depends on rank, category, branch choice, and college closing ranks.</li>
          <li>Rank prediction and college matching are estimates for decision support.</li>
        </ul>
      </div>
    </section>
  );
}