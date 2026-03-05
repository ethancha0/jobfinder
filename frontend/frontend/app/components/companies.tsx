"use client";

import React, { useEffect, useState } from "react";
import { getApiBaseUrl } from "../lib/apiBase";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import RotatingLoadingMessage from "@/components/rotating-loading";
import StatBubble from "@/components/ui/statbubble";
import { Briefcase, Building, BuildingIcon, PersonStanding, PersonStandingIcon } from "lucide-react";
import Squares from "@/components/Squares";
import PixelSnow from "@/components/PixelSnow";


type Job = {
  title: string;
  companyName: string;
  location: { name: string } | null;
  published: string | null;
  url: string | null;
  content: string | null;
};
type CompaniesResponse = { jobs: Job[]; total: number; totalSearched: number; companiesSearched:number };
type JobSearchResponse ={ jobs: Job[]; count: number;};

// date formatter for readability
function formatPublished(published: string | null): string {
  if (!published) return "Unknown";
  const d = new Date(published);
  if (Number.isNaN(d.getTime())) return published;

  const absolute = new Intl.DateTimeFormat(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(d);

  const diffDays = Math.round((d.getTime() - Date.now()) / 86_400_000);
  const diffHours = Math.round((d.getTime() - Date.now()) / 36_00_000);

  const rtf = new Intl.RelativeTimeFormat(undefined,{numeric: "auto"} );

  const relative = 
    Math.abs(diffDays) > 1
    ? rtf.format(diffDays, "day")
    : rtf.format(diffHours, "hour");



  return `${absolute} (${relative})`;
}


async function fetchCompanies(): Promise<CompaniesResponse | null> {
  try {
    const apiBase = getApiBaseUrl();
    const res = await fetch(`${apiBase}/greenhouse/alljobs`);
    if (!res.ok) {
      throw new Error("Failed to fetch companies");
    }
    return await res.json();
  } catch (error) {
    console.error("error:", error);
    return null;
  }
}


type CompaniesProps = {
  filters?: React.ReactNode;
};

export const Companies = ({ filters }: CompaniesProps) => {
  const [loading, setLoading] = useState(false);
  const [searchInput, setSearchInput] = useState("");
  const [isSearchFocused, setIsSearchFocused] = useState(false);
  const [query, setQuery] = useState("");
  const [jobs, setJobs] = useState <JobSearchResponse | null> (null);
  const [placeholderIndex, setPlaceholderIndex] = useState(0);

  const animatedPlaceholders = [
    "Search by job title, company, or keyword...",
    'Try "Data Science"',
    'Try "Product Manager"',
    'Try "Software Intern"',
  ];

  useEffect(() => {
    if (searchInput.trim().length > 0 || isSearchFocused) return;

    const intervalId = window.setInterval(() => {
      setPlaceholderIndex((prev) => (prev + 1) % animatedPlaceholders.length);
    }, 2200);

    return () => window.clearInterval(intervalId);
  }, [searchInput, isSearchFocused, animatedPlaceholders.length]);

  const handleSearch = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true)
    setQuery(searchInput)

    try{
      const apiBase = getApiBaseUrl();
      const res = await fetch(`${apiBase}/greenhouse/queryjobs?userQuery=${encodeURIComponent(searchInput)}`);

      if(!res.ok){
        throw new Error("Failed to query jobs");
      }
     const parsed =  await res.json();
    setJobs(parsed)
      console.log(parsed)
      setLoading(false)
      return
    

    }catch(error){
      console.error("error", error);
      setLoading(false)
      return null
    }
    



  };


  return (


    <div>
        <section className="relative left-1/2 right-1/2 mb-6 w-screen -translate-x-1/2 overflow-hidden border-b border-gray-300">
          <div aria-hidden="true" className="pointer-events-none absolute inset-0">
              <PixelSnow 
                color="#ffffff"
                flakeSize={0.10}
                minFlakeSize={1.25}
                pixelResolution={400}
                speed={1}
                density={0.3}
                direction={125}
                brightness={1}
                depthFade={8}
                farPlane={20}
                gamma={0.4545}
                variant="square"
            />
            <div className="absolute inset-0 bg-slate-100/90" />
          </div>

          <div className="relative z-10 mx-auto max-w-7xl px-4 py-16">
            <div className="flex flex-col items-center justify-center">
              <h1 className="text-4xl font-bold">Find your Dream Job</h1>
              <p className="p-2 text-gray-600">New jobs updated every 30 minutes</p>

              <form onSubmit={handleSearch} className="flex w-full max-w-2xl items-center gap-3">
                <div className="relative flex-1">
                  <Input
                    type="search"
                    placeholder=""
                    className="p-6"
                    value={searchInput}
                    onChange={(e) => setSearchInput(e.target.value)}
                    onFocus={() => setIsSearchFocused(true)}
                    onBlur={() => setIsSearchFocused(false)}
                    aria-label="Search jobs"
                  />
                  {!isSearchFocused && searchInput.trim().length === 0 && (
                    <span
                      aria-hidden="true"
                      className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-sm text-gray-500/90 transition-opacity duration-300 animate-pulse"
                    >
                      {animatedPlaceholders[placeholderIndex]}
                    </span>
                  )}
                </div>

                <Button type="submit" className="glass-card">Search</Button>
              </form>
              <div className="mt-5">
                {loading && (
                  <RotatingLoadingMessage/>
                )}
              </div>

              {!jobs && (
                <div className="mt-10 flex flex-wrap justify-center gap-10">
                  <StatBubble
                    Icon={BuildingIcon}
                    stat={500}
                    caption="Companies Hiring"
                  />

                  <StatBubble
                    Icon={Briefcase}
                    stat={20000}
                    caption="Active Jobs"
                  />

                  <StatBubble
                    Icon={PersonStandingIcon}
                    stat={50}
                    caption="Job Seekers"
                  />
                </div>
              )}
            </div>
          </div>
        </section>
        


        {jobs && (
          <div className="border-t border-gray-300 pt-6">
            <div
              className={`grid grid-cols-1 gap-6 lg:items-start ${
                filters
                  ? "lg:grid-cols-[260px_minmax(0,1fr)]"
                  : "lg:grid-cols-[minmax(0,820px)] lg:justify-center"
              }`}
            >
              {filters && <aside className="w-full">{filters}</aside>}

              <div className="min-w-0">
                <h1 className="glass-card mb-2 text-gray-600">
                  Showing results for "{query}"
                  <p>{jobs.count} jobs found</p>
                </h1>

                <ul className="space-y-2 p-4">
                  {jobs.jobs.map((job, i) => (
                    <li 
                    className="glass-card p-6"
                    key={i}
                    >
                      <a href={job.url ?? undefined} className="block">
                        <div className=" gap-9 sm:flex-row sm:flex-wrap sm:items-center sm:gap-6">
                          <p className="font-medium">{job.title}</p>
                          <p>{job.companyName}</p>
                          <p className="text-sm opacity-80">
                            {job.location?.name ?? "Remote/Unspecified"}
                          </p>
                          <span className="text-xs opacity-70">Posted: {formatPublished(job.published)}</span>
                        </div>
                      </a>

                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

    </div>

  );
};