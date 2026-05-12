import React from "react";

export default function InfoItem({ icon, title, text }) {
  return (
    <div className="rounded-md border border-[#d9e1ea] bg-[#f9fbfd] p-4">
      <div className="mb-2 flex items-center gap-2 text-sm font-semibold text-[#0f766e]">
        {icon}
        {title}
      </div>
      <p className="text-sm leading-5 text-[#5d6b7a]">{text}</p>
    </div>
  );
}