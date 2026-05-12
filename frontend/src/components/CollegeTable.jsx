import React from "react";

const chanceClass = {
  Safe: "bg-[#e7f6ef] text-[#17663d]",
  Possible: "bg-[#fff4d6] text-[#80620f]",
  Ambitious: "bg-[#ffe9e3] text-[#8a2f18]",
};

export default function CollegeTable({ colleges }) {
  if (!colleges.length) {
    return (
      <p className="rounded-md border border-[#d9e1ea] p-4 text-sm leading-6 text-[#5d6b7a]">
        No matching colleges found for this category and rank band.
      </p>
    );
  }

  return (
    <div className="min-w-0">
      <div className="mb-3 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <h2 className="text-base font-semibold sm:text-lg">Suggested Colleges</h2>
        <span className="w-fit rounded bg-[#eef2f6] px-2 py-1 text-xs font-semibold text-[#5d6b7a]">
          Showing {colleges.length}
        </span>
      </div>

      <p className="mb-3 text-xs text-[#5d6b7a] md:hidden">
        Swipe horizontally only if needed. Cards below are optimized for small screens.
      </p>

      {/* Mobile cards */}
      <div className="space-y-3 md:hidden">
        {colleges.map((college) => (
          <article
            key={`${college.college_name}-${college.branch_name}-${college.closing_rank}`}
            className="rounded-md border border-[#d9e1ea] bg-white p-4"
          >
            <div className="flex items-start justify-between gap-3">
              <div>
                <h3 className="text-sm font-semibold text-[#17202a]">
                  {college.college_name}
                </h3>
                <p className="mt-1 text-sm text-[#5d6b7a]">{college.branch_name}</p>
              </div>
              <span
                className={`rounded px-2 py-1 text-xs font-semibold ${
                  chanceClass[college.chance] || "bg-[#eef2f6] text-[#5d6b7a]"
                }`}
              >
                {college.chance}
              </span>
            </div>

            <dl className="mt-3 grid grid-cols-2 gap-x-4 gap-y-3 text-sm">
              <div>
                <dt className="text-xs font-semibold uppercase tracking-wide text-[#5d6b7a]">
                  Closing Rank
                </dt>
                <dd className="mt-1 text-[#17202a]">
                  {college.closing_rank.toLocaleString()}
                </dd>
              </div>

              <div>
                <dt className="text-xs font-semibold uppercase tracking-wide text-[#5d6b7a]">
                  Priority
                </dt>
                <dd className="mt-1 text-[#17202a]">
                  {college.college_priority ? `#${college.college_priority}` : "-"}
                </dd>
              </div>

              <div className="col-span-2">
                <dt className="text-xs font-semibold uppercase tracking-wide text-[#5d6b7a]">
                  Location
                </dt>
                <dd className="mt-1 text-[#17202a]">{college.location || "-"}</dd>
              </div>
            </dl>
          </article>
        ))}
      </div>

      {/* Desktop / tablet table */}
      <div className="hidden overflow-x-auto rounded-md border border-[#d9e1ea] md:block">
        <table className="w-full min-w-[680px] border-collapse text-left text-sm">
          <thead className="bg-[#eef2f6] text-xs uppercase tracking-wide text-[#5d6b7a]">
            <tr>
              <th className="px-4 py-3">College</th>
              <th className="px-4 py-3">Branch</th>
              <th className="px-4 py-3">Closing Rank</th>
              <th className="px-4 py-3">Location</th>
              <th className="px-4 py-3">Priority</th>
              <th className="px-4 py-3">Chance</th>
            </tr>
          </thead>
          <tbody>
            {colleges.map((college) => (
              <tr
                key={`${college.college_name}-${college.branch_name}-${college.closing_rank}`}
                className="border-t border-[#d9e1ea]"
              >
                <td className="px-4 py-3 font-medium">{college.college_name}</td>
                <td className="px-4 py-3">{college.branch_name}</td>
                <td className="px-4 py-3">{college.closing_rank.toLocaleString()}</td>
                <td className="px-4 py-3">{college.location || "-"}</td>
                <td className="px-4 py-3">
                  {college.college_priority ? `#${college.college_priority}` : "-"}
                </td>
                <td className="px-4 py-3">
                  <span
                    className={`rounded px-2 py-1 text-xs font-semibold ${
                      chanceClass[college.chance] || "bg-[#eef2f6] text-[#5d6b7a]"
                    }`}
                  >
                    {college.chance}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}