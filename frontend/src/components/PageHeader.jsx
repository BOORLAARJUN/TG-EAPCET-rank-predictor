import React from "react";
import { GraduationCap, Loader2 } from "lucide-react";

export default function PageHeader({ loading }) {
  return (
    <section className="border-b border-[#d9e1ea] bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-5">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-md bg-[#0f766e] text-white">
            <GraduationCap size={22} />
          </div>
          <div>
            <h1 className="text-xl font-semibold">TS EAMCET Rank Predictor</h1>
            <p className="text-sm text-[#5d6b7a]">
              Marks in, qualification status, rank band, and college matches out.
            </p>
          </div>
        </div>

        {loading && (
          <div className="flex items-center gap-2 text-sm text-[#0f766e]">
            <Loader2 className="animate-spin" size={18} />
            Processing
          </div>
        )}
      </div>
    </section>
  );
}