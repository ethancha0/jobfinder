import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from db.database import SessionLocal
from db.models import Company

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/alljobs")
def get_all_greenhouse_jobs(db:Session = Depends(get_db)):

    companies = db.query(Company).all()

    softwareInternJobs = []
    totalJobsSearched = 0
    totalCompaniesSearched = 0 
    totalJobErrors = 0 # invalid slugs 

    for company in companies:
        url =  f"https://boards-api.greenhouse.io/v1/boards/{company.board_token}/jobs?content=true"
        response = requests.get(url, timeout=6)
        totalCompaniesSearched += 1

        try:
            if response.status_code != 200:
                totalJobErrors += 1
                continue # skip bad jobs for now
            # return {"error": "Failed to fetch every softare intern jobs"}

            allJobs = response.json()
            for job in allJobs.get("jobs", []):
                totalJobsSearched += 1
                if "software" in job["title"].lower() and "intern" in job["title"].lower():
                    softwareInternJobs.append({
                        "title": job["title"],
                        "companyName": company.name,
                        "location": job["location"],
                        "published": job.get("first_published"),
                        "url": job["absolute_url"]
                    }
                    )
        except requests.exceptions.Timeout:
            print(f"Timeout for {company}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {company}: {e}")
            continue

    return {
        "jobs": softwareInternJobs,
        "total": len(softwareInternJobs),
        "totalSearched": totalJobsSearched,
        "companiesSearched": totalCompaniesSearched,
    }





@router.get("/{company_slug}")
def get_greenhouse_jobs(company_slug: str):
    url = "https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs?content=true"
    url = url.format(company_slug=company_slug)
    response = requests.get(url, timeout=6)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch jobs"}
    
    jobs = response.json()

    parsed_jobs = []
    for job in jobs["jobs"]:
        if "software" in job["title"].lower() or "intern" in job["title"].lower():
            parsed_jobs.append({
                "title": job["title"],
                "companyName": job["company_name"],
                "location": job["location"],
                "published": job["first_published"],
                "url": job["absolute_url"]
            })

    return {
        "jobs": parsed_jobs,
        "total": len(parsed_jobs)
    }


