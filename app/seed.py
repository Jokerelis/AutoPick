
from .database import Base, engine, SessionLocal
from .models import Company, Car, Reservation


def seed_database():
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:

        if db.query(Company).first():
            print("Data created already!")
            return

        company1 = Company(name="AutoPick Vilnius")
        company2 = Company(name="AutoPick Kaunas")

        db.add_all([company1, company2])
        db.flush()

        cars = [
            Car(
                company_id=company1.id,
                brand="Volkswagen",
                model="Golf",
                category="Economic",
                body_type="Hatchback",
                is_4x4=False,
                base_price=30.0
            ),
            Car(
                company_id=company1.id,
                brand="Audi",
                model="A6",
                category="Comfort",
                body_type="Sedan",
                is_4x4=False,
                base_price=45.0
            ),
            Car(
                company_id=company1.id,
                brand="Mazda",
                model="MX-5",
                category="Sport",
                body_type="Convertible",
                is_4x4=False,
                base_price=55.0
            ),
            Car(
                company_id=company1.id,
                brand="BMW",
                model="X5",
                category="Premium",
                body_type="SUV",
                is_4x4=True,
                base_price=90.0
            ),
            Car(
                company_id=company2.id,
                brand="Toyota",
                model="Yaris",
                category="Economic",
                body_type="Hatchback",
                is_4x4=False,
                base_price=30.0
            ),
            Car(
                company_id=company2.id,
                brand="BMW",
                model="320",
                category="Comfort",
                body_type="Sedan",
                is_4x4=False,
                base_price=55.0
            ),
            Car(
                company_id=company2.id,
                brand="Subaru",
                model="Forester",
                category="Economic",
                body_type="SUV",
                is_4x4=True,
                base_price=45.0
            ),
            Car(
                company_id=company2.id,
                brand="BMW",
                model="M4",
                category="Sport",
                body_type="Coupe",
                is_4x4=False,
                base_price=110.0
            )
        ]

        db.add_all(cars)
        db.commit()

        print("Duomenu baze sekmingai sukurta!")
        print("Sukurtos 2 imones ir 8 automobiliai.")


if __name__ == "__main__":
    seed_database()
