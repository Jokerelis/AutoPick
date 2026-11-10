
from datetime import date
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.models import Company, Car, Reservation
from app.demand import get_demand_multiplier
from app.pricing import calculate_price


def test_demand_and_company_filtering():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    start = date(2027, 11, 10)
    end = date(2027, 11, 13)

    with Session(engine) as db:
        company1 = Company(name="Vilnius")
        company2 = Company(name="Kaunas")

        db.add_all([company1, company2])
        db.flush()

        cars = []

        for i in range(5):
            car = Car(
                company_id=company1.id,
                brand="VW",
                model="Golf",
                category="Economic",
                body_type="Hatchback",
                is_4x4=False,
                base_price=30,
                status="Available"
            )
            db.add(car)
            cars.append(car)

        kaunas_car = Car(
            company_id=company2.id,
            brand="Toyota",
            model="Yaris",
            category="Economic",
            body_type="Hatchback",
            is_4x4=False,
            base_price=30,
            status="Available"
        )

        db.add(kaunas_car)
        db.flush()

        for car in cars[:4]:
            db.add(Reservation(
                company_id=company1.id,
                car_id=car.id,
                start_date=start,
                end_date=end,
                driver_age=30,
                driving_experience=5,
                total_price=90,
                status="Confirmed"
            ))

        db.commit()
        multiplier = get_demand_multiplier(
            db, company1.id, cars[4], start, end
        )

        assert multiplier == Decimal("1.10")

        price = calculate_price(
            30, start, end, 30, cars[4], multiplier
        )

        assert price == 99.00

        kaunas_multiplier = get_demand_multiplier(
            db, company2.id, kaunas_car, start, end
        )

        assert kaunas_multiplier == Decimal("1.00")

    engine.dispose()
