import React from "react";
import { FileUp, Search } from "lucide-react";
import MarksForm from "./MarksForm.jsx";
import FileUpload from "./FileUpload.jsx";

export default function InputPanel({ loading, onPredict, onBulkUpload }) {
  return (
    <div className="space-y-5">
      <section className="rounded-md border border-[#d9e1ea] bg-white p-4 shadow-sm sm:p-5">
        <div className="mb-4 flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-[#5d6b7a]">
          <Search size={16} />
          Single Prediction
        </div>
        <MarksForm onSubmit={onPredict} disabled={loading} />
      </section>

      <section className="rounded-md border border-[#d9e1ea] bg-white p-4 shadow-sm sm:p-5">
        <div className="mb-4 flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-[#5d6b7a]">
          <FileUp size={16} />
          CSV Upload
        </div>
        <FileUpload onUpload={onBulkUpload} disabled={loading} />
      </section>
    </div>
  );
}