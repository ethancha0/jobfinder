import requests
from fastapi import APIRouter

router = APIRouter()


@router.get("/{company_slug}")
def get_greenhouse_jobs(company_slug: str):
    url = "https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs?content=true"
    url = url.format(company_slug=company_slug)
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch jobs"}
    
    jobs = response.json()

    parsed_jobs = []
    for job in jobs["jobs"]:
        if "software" in job["title"].lower() or "intern" in job["title"].lower():
            parsed_jobs.append({
                "title": job["title"],
               # "url": job["absolute_url"],
            })

    return {
        "jobs": parsed_jobs,
        "total": len(parsed_jobs)
    }


