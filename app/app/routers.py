from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import crud
from app.db.database import get_db
from app.schemas.schemas import VacationCreate, VacationOut

router = APIRouter()


@router.post("/", response_model=VacationOut)
def create_vacation(vac: VacationCreate, db: Session = Depends(get_db)):
    try:
        return crud.add_vacation(db, vac)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/last/{employee_id}", response_model=list[VacationOut])
def last_three(employee_id: int, db: Session = Depends(get_db)):
    return crud.get_last_three_vacations(db, employee_id)


@router.get("/period", response_model=list[VacationOut])
def get_by_period(start_date: str, end_date: str, db: Session = Depends(get_db)):
    return crud.get_vacations_in_period(db, start_date, end_date)


@router.delete("/{vacation_id}")
def delete_vacation(vacation_id: int, db: Session = Depends(get_db)):
    success = crud.delete_vacation(db, vacation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vacation not found")
    return {"ok": True}
