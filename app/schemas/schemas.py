from datetime import date

from pydantic import BaseModel


class VacationCreate(BaseModel):
    employee_id: int
    start_date: date
    end_date: date


class VacationOut(VacationCreate):
    id: int

    class Config:
        orm_mode = True
