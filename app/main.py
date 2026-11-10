
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import Car
from .schemas import ReservationCreate
from .auth import get_company_id, check_company_access

from .reservation_service import (
    create_reservation,
    CarNotFoundError,
    ReservationConflictError
)

app = FastAPI(title="AutoPick API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def car_to_dict(car):
    return {
        "id": car.id,
        "company_id": car.company_id,
        "brand": car.brand,
        "model": car.model,
        "category": car.category,
        "body_type": car.body_type,
        "is_4x4": car.is_4x4,
        "base_price": car.base_price,
        "status": car.status
    }


@app.get("/")
def home():
    return {"message": "AutoPick API is running!"}


@app.get("/companies/{company_id}/cars")
def get_cars(
    company_id: int,
    authenticated_company_id: int = Depends(get_company_id),
    db: Session = Depends(get_db)
):
    check_company_access(
        company_id, authenticated_company_id
    )

    cars = db.scalars(
        select(Car).where(
            Car.company_id == authenticated_company_id
        )
    ).all()

    return [car_to_dict(car) for car in cars]


@app.get("/companies/{company_id}/cars/{car_id}")
def get_car(
    company_id: int,
    car_id: int,
    authenticated_company_id: int = Depends(get_company_id),
    db: Session = Depends(get_db)
):
    check_company_access(
        company_id, authenticated_company_id
    )

    car = db.scalar(
        select(Car).where(
            Car.id == car_id,
            Car.company_id == authenticated_company_id
        )
    )

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    return car_to_dict(car)


@app.post("/companies/{company_id}/reservations", status_code=201)
def reserve_car(
    company_id: int,
    data: ReservationCreate,
    authenticated_company_id: int = Depends(get_company_id),
    db: Session = Depends(get_db)
):
    check_company_access(
        company_id, authenticated_company_id
    )

    try:
        reservation = create_reservation(
            db, authenticated_company_id, data
        )

    except CarNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except ReservationConflictError as error:
        raise HTTPException(
            status_code=409,
            detail={
                "message": str(error),
                "alternatives": error.alternatives
            }
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "id": reservation.id,
        "company_id": reservation.company_id,
        "car_id": reservation.car_id,
        "total_price": reservation.total_price,
        "status": reservation.status
    }
