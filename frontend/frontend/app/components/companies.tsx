"use client";

import React, { useEffect, useState } from "react";
import { getApiBaseUrl } from "../lib/apiBase";

type Job = {
  title: string;
  companyName: string;
  location: { name: string } | null;
  published: string;
  url: string;
};
type CompaniesResponse = { jobs: Job[]; total: number; totalSearched: number; companiesSearched:number };

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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetchCompanies().then((result) => {
      if (cancelled) return;
      setLoading(false);
      if (result === null) {
        setError("Failed to load companies");
      } else {
        setData(result);
      }
    });
    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data) return null;

  return (
    <div>
      <h1>All Software Intern Positions: {data.total}</h1>
      <p>Out of {data.totalSearched} jobs searched and {data.companiesSearched} companies</p>
      <ul className="space-y-2">
        {data.jobs.map((job, i) => (
          <li 
          className="border border-white p-2 rounded-md"
          key={i}
          >
            <a href={job.url} className="block">
              <div className="flex flex-col gap-1 sm:flex-row sm:flex-wrap sm:items-center sm:gap-6">
                <span className="font-medium">{job.companyName}</span>
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
  );
};