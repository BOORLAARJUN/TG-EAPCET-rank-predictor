import React from "react";
import { CheckCircle2, XCircle } from "lucide-react";

export default function QualificationStatus({ prediction, compact = false }) {
  const qualified = prediction?.is_qualified;
  const message =
    prediction?.qualification_message ||
    (qualified
      ? "You meet the qualification rule for your category."
      : "You do not meet the qualification rule for your category.");

  return (
    <section
      className={`rounded-md border p-4 ${
        qualified
          ? "border-[#b9dfc5] bg-[#eefaf1]"
          : "border-[#f0b8a8] bg-[#fff4ef]"
      }`}
    >
      <div className="flex items-start gap-3">
        <div className={qualified ? "text-[#1f7a3e]" : "text-[#b5472d]"}>
          {qualified ? <CheckCircle2 size={20} /> : <XCircle size={20} />}
        </div>

        <div>
          <h3 className={`text-sm font-semibold ${qualified ? "text-[#1f5f33]" : "text-[#8a2f18]"}`}>
            {qualified ? "Qualified" : "Not Qualified"}
          </h3>
          <p className={`mt-1 text-sm leading-6 ${qualified ? "text-[#2f6b42]" : "text-[#8a2f18]"}`}>
            {message}
          </p>
          {!compact && (
            <p className="mt-2 text-xs leading-5 text-[#5d6b7a]">
              Qualification marks and admission cutoffs are different.
            </p>
          )}
        </div>
      </div>
    </section>
  );
}