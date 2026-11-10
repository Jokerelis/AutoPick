
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP


def get_season_multiplier(car, current_date):
    month = current_date.month
    if month in [6, 7, 8]:
        if car.category == "Sport" or car.body_type == "Convertible":
            return Decimal("1.15")
    if month in [12, 1, 2]:
        if car.body_type == "SUV" or car.is_4x4:
            return Decimal("1.15")

    return Decimal("1.00")


def calculate_price(
    base_price,
    start_date,
    end_date,
    driver_age,
    car,
    demand_multiplier=Decimal("1.00")
):
    days = (end_date - start_date).days

    if days <= 0:
        raise ValueError("Incorrect number of days")

    total = Decimal("0")
    daily_price = Decimal(str(base_price))

    for day in range(days):
        current_date = start_date + timedelta(days=day)

        multiplier = get_season_multiplier(
            car, current_date
        )

        total += daily_price * multiplier

    total *= demand_multiplier

    if days >= 7:
        total *= Decimal("0.90")

    if driver_age < 25:
        total *= Decimal("1.15")

    return float(total.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    ))
