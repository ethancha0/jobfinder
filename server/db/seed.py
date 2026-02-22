import csv
import logging
from db.database import SessionLocal, Base, engine
from db.models import Company
import os

logger = logging.getLogger(__name__)

def seed_companies():
    # Ensure tables exist when running the seeder directly
    Base.metadata.create_all(bind=engine)
    db = None
    try:
        db = SessionLocal()

        csv_path = os.path.join(os.path.dirname(__file__), "companies.csv")
        if not os.path.exists(csv_path):
            csv_path = os.path.join(os.path.dirname(__file__), "..", "companies.csv")

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                existing = db.query(Company).filter(
                    Company.board_token == row["board_token"]
                ).first()

                if not existing:
                    db.add(
                        Company(
                            name=row["name"],
                            board_token=row["board_token"]
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