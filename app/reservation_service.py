from datetime import date
from sqlalchemy import select

from .models import Car,Reservation
from .pricing import calculate_price
from .demand import get_demand_multiplier
from .alternatives import find_alternatives

class CarNotFoundError(Exception):
    pass

class ReservationConflictError(Exception):
    def __init__(self, message, alternatives=None):
        super().__init__(message)
        self.alternatives = alternatives or []


def create_reservation(db, company_id, data):
    if data.end_date <= data.start_date:
        raise ValueError("Incorrect reservation dates")
    if data.start_date < date.today():
        raise ValueError("Impossible to reserve the past")
    if data.driver_age < 20:
        raise ValueError("Driver has to be atleast 20 years old")
    if data.driving_experience < 1:
        raise ValueError("Driver must have atleast 1 year of driving experience")

    car = db.scalar(
        select(Car).where(
            Car.id == data.car_id,
            Car.company_id == company_id
        )
    )

    if car is None:
        raise CarNotFoundError("Car not found")
    if car.status != "Available":
        alternatives = find_alternatives(
            db, company_id, car,
            data.start_date,
            data.end_date,
            data.driver_age
        )
        raise ReservationConflictError(
            "Car is not available at these dates",
            alternatives
        )

    conflict = db.scalar(
        select(Reservation.id).where(
            Reservation.car_id == car.id,
            Reservation.company_id == company_id,
            Reservation.status == "Confirmed",
            Reservation.start_date < data.end_date,
            Reservation.end_date > data.start_date
        )
    )

    if conflict is not None:
        alternatives = find_alternatives(
            db, company_id, car,
            data.start_date,
            data.end_date,
            data.driver_age
        )
        raise ReservationConflictError(
            "Car is already reserved at these dates",
            alternatives
        )
    demand_multiplier = get_demand_multiplier(
        db,
        company_id,
        car,
        data.start_date,
        data.end_date
    )

    total_price = calculate_price(
        car.base_price,
        data.start_date,
        data.end_date,
        data.driver_age,
        car,
        demand_multiplier
    )
    reservation = Reservation(
        company_id = company_id,
        car_id = car.id,
        start_date = data.start_date,
        end_date = data.end_date,
        driver_age = data.driver_age,
        driving_experience = data.driving_experience,
        total_price = total_price,
        status = "Confirmed"
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return reservation