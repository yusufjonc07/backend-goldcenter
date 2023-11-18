import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.attandance import *
from app.schemas.attandance import *
from app.utils.pagination import pagination


def get_all_attandances(search, page, limit, usr, db: Session):
    
    attandances = db.query(Attandance)

    #if search:
        #attandances = attandances.filter(
            #Attandance.id.like(f"%{search}%"),
        #)

    return pagination(attandances, page, limit)

def create_attandance(form_data: NewAttandance, usr, db: Session):
    
    try:
        new_attandance = Attandance(
            type=form_data.type,
        employeeId=form_data.employeeid,
        workTime=form_data.worktime,
        authorizator=form_data.authorizator,
        created_at=form_data.created_at,
    )

        db.add(new_attandance)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)

def update_attandance(id, form_data: UpdateAttandance, usr, db: Session):
    
    try:
        attandance = db.query(Attandance).filter(Attandance.id == id)
        this_attandance = attandance.first()
        if this_attandance:
            attandance.update({    
            Attandance.type: form_data.type,
            Attandance.employeeId: form_data.employeeid,
            Attandance.workTime: form_data.worktime,
            Attandance.authorizator: form_data.authorizator,
            Attandance.created_at: form_data.created_at,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
    
