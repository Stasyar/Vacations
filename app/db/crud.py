from sqlalchemy.orm import Session

from app.db import models
from app.schemas.schemas import VacationCreate


def add_vacation(db: Session, vacation: VacationCreate):

    conflict = (
        db.query(models.Vacation)
        .filter(
            models.Vacation.employee_id == vacation.employee_id,
            models.Vacation.start_date <= vacation.end_date,
            models.Vacation.end_date >= vacation.start_date,
        )
        .first()
    )

    if conflict:
        raise ValueError("Vacation conflicts with existing one")

    new_vac = models.Vacation(**vacation.dict())
    db.add(new_vac)
    db.commit()
    db.refresh(new_vac)
    return new_vac


def get_last_three_vacations(db: Session, employee_id: int):
    return (
        db.query(models.Vacation)
        .filter_by(employee_id=employee_id)
        .order_by(models.Vacation.start_date.desc())
        .limit(3)
        .all()
    )


def get_vacations_in_period(db: Session, start: str, end: str):
    return (
        db.query(models.Vacation)
        .filter(models.Vacation.start_date <= end, models.Vacation.end_date >= start)
        .all()
    )


def delete_vacation(db: Session, vacation_id: int):
    vac = db.query(models.Vacation).get(vacation_id)
    if vac:
        db.delete(vac)
        db.commit()
        return True
    return False
