
from decimal import Decimal
from sqlalchemy import select

from .models import Car, Reservation


def get_demand_multiplier(
    db, company_id, car, start_date, end_date
):
    cars = db.scalars(
        select(Car).where(
            Car.company_id == company_id,
            Car.category == car.category,
            Car.status == "Available"
        )
    ).all()
    total_cars = len(cars)
    if total_cars == 0:
        return Decimal("1.00")

    occupied_cars = 0

    for category_car in cars:

        reservation = db.scalar(
            select(Reservation.id).where(
                Reservation.company_id == company_id,
                Reservation.car_id == category_car.id,
                Reservation.status == "Confirmed",
                Reservation.start_date < end_date,
                Reservation.end_date > start_date
            )
        )

        if reservation is not None:
            occupied_cars += 1

    if occupied_cars * 100 >= total_cars * 80:
        return Decimal("1.10")

    return Decimal("1.00")
