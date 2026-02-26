"use client";

import React, { useEffect, useState } from "react";
import { getApiBaseUrl } from "../lib/apiBase";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import RotatingLoadingMessage from "@/components/rotating-loading";


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



export const Companies = () => {
  const [loading, setLoading] = useState(false);
  const [searchInput, setSearchInput] = useState("");
  const [query, setQuery] = useState("");
  const [jobs, setJobs] = useState <JobSearchResponse | null> (null);

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
        <div className="flex flex-col items-center justify-center m-20">
          <h1 className="text-4xl font-bold">Find your Dream Job</h1>
          <p className="text-gray-600">Search through thousands of job opportunities right as they come out</p>

          <form onSubmit={handleSearch}>
              <Input 
              type="search"
              placeholder="Search by job title, company, or keyword..." 
              className="p-8 w-md" 
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              />
              <Button type="submit" className="glass-card">Search</Button>
              
          </form>
          <div className="mt-5">
            {loading && (
              <RotatingLoadingMessage/>   
            )}
          </div>
          

        </div>
        


        {jobs && (

        <div>
          <div className="border border-t-1 border-gray-300 m-6"></div>

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
        )}

    </div>

  );
};