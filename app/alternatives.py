from sqlalchemy import select

from .models import Car, Reservation
from .pricing import calculate_price
from .demand import get_demand_multiplier

def find_alternatives(
        db, company_id, original_car,
        start_date, end_date, driver_age
):
    cars = db.scalars(
        select(Car).where(
            Car.company_id == company_id,
            Car.category == original_car.category,
            Car.id != original_car.id,
            Car.status == "Available"
        ).order_by(Car.base_price)
    ).all()
    alternatives = []

    for car in cars:
        conflict = db.scalar(
            select(Reservation.id).where(
                Reservation.company_id == company_id,
                Reservation.car_id == car.id,
                Reservation.status == "Confirmed",
                Reservation.start_date < end_date,
                Reservation.end_date > start_date
            )
        )
        if conflict is not None:
            continue

        demand = get_demand_multiplier(db, company_id, car, start_date, end_date)
        price = calculate_price(car.base_price,start_date,end_date,driver_age,car,demand)
        alternatives.append({
            "car_id": car.id,
            "brand": car.brand,
            "model": car.model,
            "category": car.category,
            "total_price": price
        })

        if len(alternatives) >= 3:
            break

    return alternatives
