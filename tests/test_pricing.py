
from datetime import date
from types import SimpleNamespace

import pytest

from app.pricing import calculate_price


def make_car(category, body_type, is_4x4=False):
    return SimpleNamespace(
        category=category,
        body_type=body_type,
        is_4x4=is_4x4
    )


def test_normal_price():
    car = make_car("Economic", "Hatchback")

    price = calculate_price(
        30,
        date(2026, 11, 10),
        date(2026, 11, 13),
        30,
        car
    )

    assert price == 90.00


def test_summer_sport_car():
    car = make_car("Sport", "Coupe")

    price = calculate_price(
        30,
        date(2027, 7, 10),
        date(2027, 7, 13),
        30,
        car
    )

    assert price == 103.50


def test_winter_suv():
    car = make_car("Premium", "SUV", True)

    price = calculate_price(
        30,
        date(2026, 12, 10),
        date(2026, 12, 13),
        30,
        car
    )

    assert price == 103.50


def test_long_rental_young_driver():
    car = make_car("Economic", "Hatchback")

    price = calculate_price(
        30,
        date(2026, 12, 10),
        date(2026, 12, 17),
        22,
        car
    )

    assert price == 217.35


def test_season_transition():
    car = make_car("Sport", "Convertible")

    price = calculate_price(
        30,
        date(2027, 8, 30),
        date(2027, 9, 2),
        30,
        car
    )

    assert price == 99.00


def test_invalid_dates():
    car = make_car("Economic", "Hatchback")

    with pytest.raises(ValueError):
        calculate_price(
            30,
            date(2026, 12, 15),
            date(2026, 12, 10),
            30,
            car
        )
