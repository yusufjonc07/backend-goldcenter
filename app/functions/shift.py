import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.shift import *
from app.schemas.shift import *

def get_all_shifts(search, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit
    
    shifts = db.query(Shift)

    #if search:
       #shifts = shifts.filter(
           #Shift.id.like(f"%{search}%"),
       #)

    
    all_data = shifts.order_by(Shift.id.desc()).offset(offset).limit(limit)
    count_data = shifts.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }

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
    
