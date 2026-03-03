import csv
import logging
from db.database import SessionLocal, Base, engine
from db.models import Company
import os

logger = logging.getLogger(__name__)


def _resolve_companies_csv_path() -> str:
    base_dir = os.path.dirname(__file__)
    candidate_paths = [
        os.path.join(base_dir, "..", "companies.cleaned.csv"),
        os.path.join(base_dir, "companies.cleaned.csv"),
        os.path.join(base_dir, "companies.csv"),
        os.path.join(base_dir, "..", "companies.csv"),
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            return path

    # Fall back to historical location for clearer error messages on open.
    return os.path.join(base_dir, "..", "companies.csv")


def seed_companies():
    # Ensure tables exist when running the seeder directly
    Base.metadata.create_all(bind=engine)
    db = None
    try:
        db = SessionLocal()

        csv_path = _resolve_companies_csv_path()
        logger.info("Seeding companies from CSV path: %s", csv_path)

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                name = (row.get("name") or "").strip()
                board_token = (row.get("board_token") or "").strip()

                if not name or not board_token:
                    continue

                existing = db.query(Company).filter(
                    Company.board_token == board_token
                ).first()

                if not existing:
                    db.add(
                        Company(
                            name=name,
                            board_token=board_token
                        )
                    )

        db.commit()
        print("✅ Companies seeded successfully.")
    except Exception:
        if db is not None:
            db.rollback()
        logger.exception("Error seeding companies")
        raise
    finally:
        if db is not None:
            db.close()


if __name__ == "__main__":
    seed_companies()