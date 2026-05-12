import React, { useState } from "react";

export default function FileUpload({ onUpload, disabled }) {
  const [file, setFile] = useState(null);

  function submit(event) {
    event.preventDefault();
    if (file) onUpload(file);
  }

  return (
    <form className="space-y-4" onSubmit={submit}>
      <input
        type="file"
        accept=".csv"
        className="w-full rounded-md border border-dashed border-[#9aa8b7] p-3 text-sm"
        onChange={(event) => setFile(event.target.files?.[0] || null)}
      />
      <button disabled={disabled || !file} className="w-full rounded-md border border-[#0f766e] px-4 py-2 font-semibold text-[#0f766e] hover:bg-[#eef8f6] disabled:cursor-not-allowed disabled:border-[#9aa8b7] disabled:text-[#9aa8b7]">
        Upload CSV
      </button>
    </form>
  );
}
