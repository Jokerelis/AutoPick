from datetime import date
from pydantic import BaseModel, Field

class ReservationCreate(BaseModel):
    car_id: int = Field(gt=0)
    start_date: date
    end_date: date
    driver_age: int = Field(ge=0)
    driving_experience: float = Field(gt=0)
