import React from "react";
import { Loader2, Youtube } from "lucide-react";

export default function PageHeader({ loading }) {
  return (
    <section className="border-b border-[#d9e1ea] bg-[#07101c] text-white">
      <div className="mx-auto flex max-w-7xl flex-col gap-4 px-5 py-5 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex min-w-0 items-center gap-3">
          <img
            src="/upforge-icon.png"
            alt="UpForge logo"
            className="h-12 w-12 shrink-0 rounded-md border border-[#1df2ff]/35 object-cover shadow-[0_0_22px_rgba(29,242,255,0.32)]"
          />
          <div>
            <h1 className="text-xl font-semibold leading-tight">UpForge</h1>
            <p className="text-sm leading-6 text-[#b7c7d8]">
              TG EAPCET 2026 engineering rank prediction with student guidance, coding tutorials, and career direction.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <a
            href="https://youtube.com/@upforge77?si=J43Cms66r5N6RECU"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 rounded-md border border-[#1df2ff]/35 px-3 py-2 text-sm font-semibold text-[#dffcff] hover:bg-[#112437]"
          >
            <Youtube size={17} />
            Watch UpForge
          </a>

          {loading && (
            <div className="flex items-center gap-2 text-sm text-[#2ff7ca]">
              <Loader2 className="animate-spin" size={18} />
              Processing
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
