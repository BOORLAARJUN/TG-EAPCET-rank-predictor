import React from "react";
import { BarChart3, GraduationCap, ListChecks } from "lucide-react";
import InfoItem from "./InfoItem.jsx";

export default function InfoGrid() {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">
      <InfoItem
        icon={<BarChart3 size={18} />}
        title="Rank estimate"
        text="Uses TG EAPCET 2026 engineering marks and the trained marks-rank curve to estimate a likely rank band."
      />
      <InfoItem
        icon={<ListChecks size={18} />}
        title="College matching"
        text="Compares that rank with engineering final-phase cutoff ranks and your category, branch, and college priority order."
      />
      <InfoItem
        icon={<GraduationCap size={18} />}
        title="Decision support"
        text="Shows qualification status, 2026 shift adjustment estimates, and Safe, Possible, or Ambitious college labels."
      />
    </div>
  );
}
