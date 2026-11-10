
from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.models import Company, Car, Reservation
from app.schemas import ReservationCreate
from app.reservation_service import (
    create_reservation,
    ReservationConflictError
)

def test_alternative_same_company():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as db:
        vilnius = Company(name="Vilnius")
        kaunas = Company(name="Kaunas")

        db.add_all([vilnius, kaunas])
        db.flush()

        car1 = Car(
            company_id=vilnius.id,
            brand="VW",
            model="Golf",
            category="Economic",
            body_type="Hatchback",
            is_4x4=False,
            base_price=30,
            status="Available"
        )

        car2 = Car(
            company_id=vilnius.id,
            brand="Toyota",
            model="Yaris",
            category="Economic",
            body_type="Hatchback",
            is_4x4=False,
            base_price=30,
            status="Available"
        )

        car3 = Car(
            company_id=kaunas.id,
            brand="Ford",
            model="Focus",
            category="Economic",
            body_type="Hatchback",
            is_4x4=False,
            base_price=30,
            status="Available"
        )

        db.add_all([car1, car2, car3])
        db.flush()
        db.add(Reservation(
            company_id=vilnius.id,
            car_id=car1.id,
            start_date=date(2027, 5, 10),
            end_date=date(2027, 5, 13),
            driver_age=30,
            driving_experience=5,
            total_price=90,
            status="Confirmed"
        ))

        db.commit()

        data = ReservationCreate(
            car_id=car1.id,
            start_date=date(2027, 5, 10),
            end_date=date(2027, 5, 13),
            driver_age=30,
            driving_experience=5
        )

        with pytest.raises(
            ReservationConflictError
        ) as error:
            create_reservation(db, vilnius.id, data)

        alternatives = error.value.alternatives

        assert len(alternatives) == 1
        assert alternatives[0]["car_id"] == car2.id
        assert alternatives[0]["total_price"] == 90.0

        assert car3.id not in [
            car["car_id"] for car in alternatives
        ]

    engine.dispose()
