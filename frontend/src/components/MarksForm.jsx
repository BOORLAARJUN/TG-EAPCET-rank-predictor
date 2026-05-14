import React, { useState } from "react";

const categories = ["OC", "BC_A", "BC_B", "BC_C", "BC_D", "BC_E", "SC_I", "SC_II", "SC_III", "ST", "EWS"];
const branches = [
  { label: "All branches", value: "" },
  { label: "Computer Science and Engineering", value: "Computer Science" },
  { label: "CSE - Artificial Intelligence and Machine Learning", value: "Artificial Intelligence" },
  { label: "CSE - Data Science", value: "Data Science" },
  { label: "CSE - Cyber Security", value: "Cyber Security" },
  { label: "CSE - Internet of Things", value: "IOT" },
  { label: "Electronics and Communication Engineering", value: "Electronics and Communication" },
  { label: "Electrical and Electronics Engineering", value: "Electrical and Electronics" },
  { label: "Information Technology", value: "Information Technology" },
  { label: "Mechanical Engineering", value: "Mechanical" },
  { label: "Civil Engineering", value: "Civil" },
];
const examShifts = [
  { label: "May 9, 2026 Shift 1", value: "2026-05-09-S1" },
  { label: "May 9, 2026 Shift 2", value: "2026-05-09-S2" },
  { label: "May 10, 2026 Shift 1", value: "2026-05-10-S1" },
  { label: "May 10, 2026 Shift 2", value: "2026-05-10-S2" },
  { label: "May 11, 2026 Shift 1", value: "2026-05-11-S1" },
  { label: "May 11, 2026 Shift 2", value: "2026-05-11-S2" },
];

export default function MarksForm({ onSubmit, disabled }) {
  const [values, setValues] = useState({
    exam_type: "TS_EAMCET",
    exam_year: 2026,
    category: "OC",
    total_marks: 124,
    branch_preference: "Computer Science",
    use_estimated_normalization: false,
    shift_id: "2026-05-09-S1",
  });

  function update(field, value) {
    setValues((current) => ({ ...current, [field]: value }));
  }

  function submit(event) {
    event.preventDefault();
    onSubmit({
      exam_type: values.exam_type,
      exam_year: Number(values.exam_year),
      category: values.category,
      total_marks: Number(values.total_marks),
      branch_preference: values.branch_preference || null,
      use_estimated_normalization: values.use_estimated_normalization,
      shift_id: values.use_estimated_normalization ? values.shift_id : null,
    });
  }

  return (
    <form className="space-y-4" onSubmit={submit}>
      <label className="block text-sm font-medium">
        Exam Type
        <select className="mt-1 w-full rounded-md border border-[#cbd5df] px-3 py-2" value={values.exam_type} onChange={(event) => update("exam_type", event.target.value)}>
          <option value="TS_EAMCET">TG EAPCET 2026 Engineering</option>
        </select>
      </label>
      <div className="grid grid-cols-2 gap-3">
        <label className="block text-sm font-medium">
          Year
          <select className="mt-1 w-full rounded-md border border-[#cbd5df] px-3 py-2" value={values.exam_year} onChange={(event) => update("exam_year", event.target.value)}>
            <option value={2026}>2026</option>
          </select>
        </label>
        <label className="block text-sm font-medium">
          Category
          <select className="mt-1 w-full rounded-md border border-[#cbd5df] px-3 py-2" value={values.category} onChange={(event) => update("category", event.target.value)}>
            {categories.map((category) => (
              <option key={category}>{category}</option>
            ))}
          </select>
        </label>
      </div>
      <label className="block text-sm font-medium">
        Total Marks
        <input type="number" min="0" max="160" step="0.01" required className="mt-1 w-full rounded-md border border-[#cbd5df] px-3 py-2" value={values.total_marks} onChange={(event) => update("total_marks", event.target.value)} />
      </label>
      <label className="block text-sm font-medium">
        Branch Preference
        <select className="mt-1 w-full rounded-md border border-[#cbd5df] px-3 py-2" value={values.branch_preference} onChange={(event) => update("branch_preference", event.target.value)}>
          {branches.map((branch) => (
            <option key={branch.label} value={branch.value}>
              {branch.label}
            </option>
          ))}
        </select>
      </label>
      <label className="flex items-start gap-3 rounded-md border border-[#d9e1ea] bg-[#f9fbfd] p-3 text-sm font-medium">
        <input
          type="checkbox"
          className="mt-1 h-4 w-4 rounded border-[#9aa8b6] text-[#0f766e]"
          checked={values.use_estimated_normalization}
          onChange={(event) => update("use_estimated_normalization", event.target.checked)}
        />
        <span>
          Apply estimated normalization
          <span className="block text-xs font-normal leading-5 text-[#5d6b7a]">
            Uses 2026 engineering shift difficulty reports for an unofficial estimate.
          </span>
        </span>
      </label>
      {values.use_estimated_normalization && (
        <label className="block text-sm font-medium">
          Exam shift
          <select className="mt-1 w-full rounded-md border border-[#cbd5df] px-3 py-2" value={values.shift_id} onChange={(event) => update("shift_id", event.target.value)}>
            {examShifts.map((shift) => (
              <option key={shift.value} value={shift.value}>
                {shift.label}
              </option>
            ))}
          </select>
        </label>
      )}
      <button disabled={disabled} className="w-full rounded-md bg-[#0f766e] px-4 py-2 font-semibold text-white hover:bg-[#115e59] disabled:cursor-not-allowed disabled:bg-[#8bb9b4]">
        Predict Rank
      </button>
    </form>
  );
}
