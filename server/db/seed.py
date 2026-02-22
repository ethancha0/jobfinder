import csv
from db.database import SessionLocal, Base, engine
from db.models import Company


def seed_companies():
    # Ensure tables exist when running the seeder directly
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    with open("companies.csv", newline="") as csvfile:
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
    db.close()
    print("✅ Companies seeded successfully.")


if __name__ == "__main__":
    seed_companies()