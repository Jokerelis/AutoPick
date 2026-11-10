
from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app, get_db
from app.models import Company, Car, Reservation


def test_company_data_isolation(monkeypatch):
    monkeypatch.setenv(
        "AUTOPICK_VILNIUS_KEY", "VilniusTestKey123"
    )
    monkeypatch.setenv(
        "AUTOPICK_KAUNAS_KEY", "KaunasTestKey456"
    )

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(engine)

    with Session(engine) as db:
        company1 = Company(name="Vilnius")
        company2 = Company(name="Kaunas")

        db.add_all([company1, company2])
        db.flush()

        car1 = Car(
            company_id=company1.id,
            brand="VW",
            model="Golf",
            category="Economic",
            body_type="Hatchback",
            is_4x4=False,
            base_price=30,
            status="Available"
        )

        car2 = Car(
            company_id=company2.id,
            brand="Toyota",
            model="Yaris",
            category="Economic",
            body_type="Hatchback",
            is_4x4=False,
            base_price=30,
            status="Available"
        )

        db.add_all([car1, car2])
        db.flush()

        other_car_id = car2.id
        db.commit()

    def override_get_db():
        with Session(engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            vilnius_headers = {
                "X-API-Key": "VilniusTestKey123"
            }
            kaunas_headers = {
                "X-API-Key": "KaunasTestKey456"
            }

            response = client.get(
                "/companies/1/cars",
                headers=vilnius_headers
            )

            assert response.status_code == 200
            assert len(response.json()) == 1
            assert response.json()[0]["model"] == "Golf"

            response = client.get(
                "/companies/2/cars",
                headers=vilnius_headers
            )

            assert response.status_code == 403

            response = client.get(
                f"/companies/1/cars/{other_car_id}",
                headers=vilnius_headers
            )

            assert response.status_code == 404

            response = client.post(
                "/companies/1/reservations",
                headers=vilnius_headers,
                json={
                    "car_id": other_car_id,
                    "start_date": "2027-05-10",
                    "end_date": "2027-05-13",
                    "driver_age": 30,
                    "driving_experience": 5
                }
            )

            assert response.status_code == 404

            response = client.post(
                "/companies/2/reservations",
                headers=vilnius_headers,
                json={
                    "car_id": other_car_id,
                    "start_date": "2027-05-10",
                    "end_date": "2027-05-13",
                    "driver_age": 30,
                    "driving_experience": 5
                }
            )

            assert response.status_code == 403

            response = client.get(
                "/companies/2/cars",
                headers=kaunas_headers
            )

            assert response.status_code == 200
            assert response.json()[0]["model"] == "Yaris"

            with Session(engine) as db:
                count = db.scalar(
                    select(func.count(Reservation.id))
                )
                assert count == 0

    finally:
        app.dependency_overrides.clear()
        engine.dispose()
