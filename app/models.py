from sqlalchemy import (
    Column, Integer, String, Float, Date, ForeignKey, Boolean
)

from .database import Base

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    company_id = Column(
        Integer,
        ForeignKey('companies.id'),
        nullable=False
    )
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    body_type = Column(String(50), nullable=False)
    is_4x4 = Column(Boolean, nullable=False)
    base_price = Column(Float, nullable=False)
    status = Column(String(30), default = "Available")


class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    company_id = Column(
        Integer,
        ForeignKey('companies.id'),
        nullable=False
    )
    car_id = Column(
        Integer,
        ForeignKey('cars.id'),
        nullable=False
    )

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    driver_age = Column(Integer, nullable=False)
    driving_experience = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(30), default = "Confirmed")