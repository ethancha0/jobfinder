import React from "react";

type JobProps = {
  company: string;
  position: string;
  location: string;
  date: Date;
};

export default function Job({ company, position, location, date }: JobProps) {
  return (
    <div className="glass-card p-4">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <div>
          <p className="font-medium">{position}</p>
          <p className="opacity-90">{company}</p>
        </div>
        <p className="text-xs opacity-70">{date.toLocaleDateString()}</p>
      </div>
      <p className="mt-1 text-sm opacity-80">{location}</p>
    </div>
  );
}
