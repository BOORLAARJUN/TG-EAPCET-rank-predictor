import React from "react";
import { Code2, Compass, Flame, GraduationCap, Youtube } from "lucide-react";

const tracks = [
  { icon: <Compass size={17} />, label: "EAPCET guidance" },
  { icon: <GraduationCap size={17} />, label: "Mentorship" },
  { icon: <Code2 size={17} />, label: "Coding tutorials" },
  { icon: <Flame size={17} />, label: "Motivation" },
];

export default function UpForgePromo() {
  return (
    <section className="overflow-hidden rounded-md border border-[#b8dce8] bg-[#07101c] text-white shadow-sm">
      <div className="grid gap-0 lg:grid-cols-[1fr_340px]">
        <div className="p-4 sm:p-5">
          <div className="mb-3 flex items-center gap-3">
            <img
              src="/upforge-icon.png"
              alt="UpForge logo"
              className="h-11 w-11 rounded-md border border-[#1df2ff]/35 object-cover shadow-[0_0_20px_rgba(47,247,202,0.28)]"
            />
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-[#2ff7ca]">Student growth channel</p>
              <h2 className="text-lg font-semibold leading-tight">Keep building after the rank estimate</h2>
            </div>
          </div>

          <p className="max-w-3xl text-sm leading-6 text-[#c7d8e8]">
            UpForge helps students move from marks and college choices to the next step:
            guidance, mentorship, career advice, coding tutorials, and the motivation to keep improving.
          </p>

          <div className="mt-4 grid grid-cols-2 gap-2 md:grid-cols-4">
            {tracks.map((track) => (
              <div key={track.label} className="flex min-h-11 items-center gap-2 rounded-md border border-white/10 bg-white/[0.06] px-3 py-2 text-sm text-[#e7f8ff]">
                <span className="text-[#2ff7ca]">{track.icon}</span>
                <span>{track.label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-col justify-between border-t border-white/10 bg-white/[0.05] p-4 sm:p-5 lg:border-l lg:border-t-0">
          <p className="text-sm font-semibold leading-6 text-[#e7f8ff]">
            Before choosing a branch, learn what that path actually looks like.
          </p>
          <a
            href="https://youtube.com/@upforge77?si=J43Cms66r5N6RECU"
            target="_blank"
            rel="noreferrer"
            className="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-md bg-[#15d8ff] px-4 py-2.5 text-sm font-bold text-[#03111c] hover:bg-[#2ff7ca]"
          >
            <Youtube size={18} />
            Find UpForge on YouTube
          </a>
        </div>
      </div>
    </section>
  );
}
