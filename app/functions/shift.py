import math
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.shift import *
from app.schemas.shift import *
from app.utils.pagination import pagination 


def get_all_shifts(search, page, limit, usr, db: Session):
    
    shifts = db.query(Shift)

    #if search:
       #shifts = shifts.filter(
           #Shift.id.like(f"%{search}%"),
       #)
    
    return pagination(shifts, page, limit)


def create_shift(form_data: NewShift, usr, db: Session):
    
    try:
        new_shift = Shift(
            name=form_data.name,
        workBeginTime=form_data.workbegintime,
        period=form_data.period,
    )

        db.add(new_shift)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)

def update_shift(id, form_data: UpdateShift, usr, db: Session):
    
    try:
        shift = db.query(Shift).filter(Shift.id == id)
        this_shift = shift.first()
        if this_shift:
            shift.update({    
            Shift.name: form_data.name,
            Shift.workBeginTime: form_data.workbegintime,
            Shift.period: form_data.period,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
    
