# JobFinder
![ScreenRecording2026-03-04at9 32 28PM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/3d2ac3b4-ac55-4eff-8462-85d7f1a3a410)

JobFinder is a job search platform that aggregates roles from public Greenhouse job boards and presents them through a fast, searchable UI.

Built as an end-to-end product project, it demonstrates API integration at scale, background data pipelines, PostgreSQL modeling, and a modern frontend experience with Next.js.

## Why This Project Stands Out

- **Real-world ingestion pipeline:** pulls live data from many external hiring boards, normalizes it, and stores it in PostgreSQL for fast querying.
- **Production-minded backend:** includes idempotent seeders, guarded internal cron endpoints, CORS configuration, and startup-safe initialization.
- **User-centric frontend:** responsive search UX, animated loading states, relative date formatting, and polished visual design.
- **Operational touches:** CSV validation tooling, failure tracking, and optional email alerts for newly discovered jobs.
- **Cloud deployment readiness:** architecture is already aligned with a typical `Vercel (frontend) + Render (backend + Postgres)` setup.

## Product Overview

JobFinder helps candidates discover new roles quickly by:

1. Loading company Greenhouse board tokens from a curated CSV
2. Validating tokens and seeding company records
3. Fetching recent jobs from Greenhouse APIs
4. Upserting jobs into PostgreSQL and optionally emailing new postings
5. Exposing APIs for full fetch and keyword-based querying
6. Rendering results in a searchable, modern web UI

## Tech Stack

### Frontend
- Next.js 16 (App Router)
- React 19 + TypeScript
- Tailwind CSS 4
- Radix/shadcn-style UI primitives
- Motion/GSAP + custom visual components

### Backend
- FastAPI
- SQLAlchemy 2
- PostgreSQL (via `psycopg2-binary`)
- Requests for Greenhouse API integration
- Resend for email notifications

## System Architecture

```text
Next.js Client (Vercel/local)
        |
        v
FastAPI Service (Render/local)  --->  Greenhouse Boards API
        |
        v
PostgreSQL (companies + jobs)
        |
        v
Optional Resend Email Notifications
```

### Core Backend Modules
- `server/main.py`  
  App bootstrapping, CORS, router registration, startup seed flow.
- `server/db/seed.py`  
  Seeds company records from CSV (`companies.cleaned.csv` preferred).
- `server/db/seed_jobs.py`  
  Fetches recent jobs, performs upserts, tracks failures, triggers emails for new jobs.
- `server/clients/greenhouse.py`  
  Public API endpoints for all jobs and query-based filtering.
- `server/routers/internal.py`  
  Token-protected internal endpoint for scheduled seeding jobs.
- `server/notifications/emails.py`  
  Resend integration for notification delivery.

### Data Model
- `companies`
  - `id` (UUID, PK)
  - `name`
  - `board_token` (unique)
  - `active`
  - `created_at`
- `jobs`
  - `id` (UUID, PK)
  - `company_id` (FK -> companies)
  - `greenhouse_job_id`
  - `title`, `location_name`, `published_at`, `url`, `content`
  - `is_active`, `emailed`, timestamps
  - Unique constraint on (`company_id`, `greenhouse_job_id`) for idempotent upserts

## Key Features

- **Keyword job search** across title, company, and location
- **Recent-job ingestion** with configurable lookback window
- **Automatic startup seeding** to preload data in deployed environments
- **CSV token validation** pipeline with cleaned + invalid report outputs
- **Failure capture** for non-200 responses, timeouts, and request errors
- **Email alert workflow** for newly inserted jobs
- **Rich UI polish** including animated placeholders, loading messages, and visual effects

## API Endpoints

Base URL (local): `http://localhost:8000`

### Public
- `GET /greenhouse/alljobs`  
  Fetches software/intern-focused jobs from all active companies.
- `GET /greenhouse/queryjobs?userQuery=<query>`  
  Searches persisted jobs using AND-based keyword matching.
- `GET /companies/`  
  Lists all companies in DB.
- `POST /companies/bulk`  
  Inserts company records (ignores existing `board_token`s).
- `GET /`  
  Health-style root endpoint.

### Internal / Operational
- `POST /internal/seed` (hidden from schema)  
  Protected by `x-seed-token` header (`SEED_CRON_TOKEN`).
- `POST /emails/` and `POST /emails/send-jobs`  
  Manual and payload-driven email actions.

Interactive docs are available at `http://localhost:8000/docs` when running locally.

## Local Development Setup

## 1) Clone and install dependencies

### Backend
```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend/frontend
npm install
```

## 2) Configure environment variables

### Backend (`server/.env`)

Required:

```env
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<db_name>
```

Optional but recommended:

```env
# Startup job seeding toggle (default enabled)
SEED_JOBS_ON_STARTUP=1

# Lookback window used by startup seeder in main.py
SEED_JOB_DAYS=14

# Lookback window used by /internal/seed endpoint
SEED_JOBS_DAYS=1

# Internal cron protection
SEED_CRON_TOKEN=your_secure_token

# Email notifications (Resend)
RESEND_API_KEY=re_xxx
ALERT_EMAIL_TO=you@example.com,teammate@example.com
ALERT_EMAIL_FROM=JobFinder <alerts@yourdomain.com>
```

### Frontend (`frontend/frontend/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 3) Validate and seed company data (optional but recommended)

```bash
cd server
python3 scripts/validate_companies_csv.py
python3 -m db.seed
```

Validation outputs:
- `server/companies.cleaned.csv`
- `server/companies.invalid.csv`

## 4) Run both services

### Backend
```bash
cd server
source .venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend/frontend
npm run dev
```

Open `http://localhost:3000`.

## Deployment Notes

- Frontend defaults to a production API URL when `NEXT_PUBLIC_API_URL` is not set in production mode.
- Backend is configured for startup seeding and CORS allow-listing to support hosted frontend domains.
- Recommended production wiring:
  - **Frontend:** Vercel
  - **Backend + DB:** Render (or equivalent managed container + Postgres)
  - **Scheduled refresh:** call `POST /internal/seed` with `x-seed-token`

## Engineering Highlights Recruiters Can Ask About

- Designing idempotent upsert logic with uniqueness constraints
- Handling flaky third-party APIs with retries, timeouts, and failure reporting
- Balancing startup performance by offloading ingestion to a daemon thread
- Building a searchable API and translating it into a clean frontend query UX
- Implementing secure internal maintenance routes for scheduled jobs
- Structuring a full-stack app for independent frontend/backend deployment

## Roadmap

- User accounts and personalized job tracking
- Saved searches and notification preferences
- Deeper ranking/relevance scoring
- Pagination + advanced filters (location, date window, seniority)
- Automated test suite (unit + integration + API contract tests)

## Repository Layout

```text
jobfinder/
├── frontend/
│   └── frontend/        # Next.js app
└── server/              # FastAPI app, DB models, seeders, scripts
```

## Author

Built by Ethan Chao as a practical full-stack engineering project focused on production-style job data ingestion and search experience.
