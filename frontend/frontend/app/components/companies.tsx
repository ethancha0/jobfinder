"use client";

import React, { useEffect, useState } from "react";

type Job = { title: string };
type CompaniesResponse = { jobs: Job[]; total: number };

async function fetchCompanies(): Promise<CompaniesResponse | null> {
  try {
    const res = await fetch("http://localhost:8000/greenhouse/stripe");
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
    setLoading(true);
    setError(null);
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
      <h1>Companies (Stripe) – {data.total} jobs</h1>
      <ul>
        {data.jobs.map((job, i) => (
          <li 
          className="border border-white p-2 rounded-md mt-2"
          key={i}
          >
            <a href={job.url}>
              {job.title}
            </a>

          </li>
        ))}
      </ul>
    </div>
  );
};