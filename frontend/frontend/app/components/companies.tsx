"use client";

import React, { useEffect, useState } from "react";
import { getApiBaseUrl } from "../lib/apiBase";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";


type Job = {
  title: string;
  companyName: string;
  location: { name: string } | null;
  published: string;
  url: string;
};
type CompaniesResponse = { jobs: Job[]; total: number; totalSearched: number; companiesSearched:number };
type JobSearchResponse ={ jobs: Job[]; count: number;};


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
  const [data, setData] = useState<CompaniesResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchInput, setSearchInput] = useState("");
  const [query, setQuery] = useState("");
  const [jobs, setJobs] = useState <JobSearchResponse | null> (null);

  const handleSearch = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
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
      return
    

    }catch(error){
      console.error("error", error);
      return null
    }
    



  };


  return (


    <div>
 

        <form onSubmit={handleSearch}>
          <Input 
          type="search"
          placeholder="Search..." 
          className="p-8 w-md" 
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          />
          <Button type="submit" className="glass-card">Search</Button>
        </form>

        <Button 
        className="glass-card p-4"
        type="submit" 
        //onClick={() => setShowJobs(true)}
        >
          Show all Jobs 
        </Button>

      
      {/*query ? (
        <p className="glass-card mt-4 mb-6">
          Showing {filteredJobs.length} result{filteredJobs.length === 1 ? "" : "s"}{" "}
          for &quot;{query}&quot;
        </p>
      ) : null*/}
        
  

        {jobs && (
        <div>
      <h1 className="glass-card mb-2">
         Showing results for {query}
      </h1>
      <p className="glass-card mb-10"> {jobs.count} jobs found </p>
      <ul className="space-y-2">
        {jobs.jobs.map((job, i) => (
          <li 
          className="glass-card"
          key={i}
          >
            <a href={job.url} className="block">
              <div className="flex flex-col gap-1 sm:flex-row sm:flex-wrap sm:items-center sm:gap-6">
                <span className="font-medium">{job.company_name}</span>
                <span>{job.title}</span>
                <span className="text-sm opacity-80">
                  {job.location?.name ?? "Remote/Unspecified"}
                </span>
                <span className="text-xs opacity-70">{job.published}</span>
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