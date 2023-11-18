import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.floor import *
from app.schemas.floor import *
from app.utils.pagination import pagination 


def get_all_floors(search, page, limit, usr, db: Session):
    
    floors = db.query(Floor)

    #if search:
       #floors = floors.filter(
           #Floor.id.like(f"%{search}%"),
       #)

    return pagination(floors, page, limit)

    

def create_floor(form_data: NewFloor, usr, db: Session):
    
    try:
        new_floor = Floor(
            name=form_data.name,
            number=form_data.number,
            description=form_data.description,
            coridorCleaningCost=form_data.coridorCleaningCost,
            branchId=form_data.branchid,
            type=form_data.type,
        )

        db.add(new_floor)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)

def update_floor(id, form_data: UpdateFloor, usr, db: Session):
    
    try:
        floor = db.query(Floor).filter(Floor.id == id)
        this_floor = floor.first()
        if this_floor:
            floor.update({    
            Floor.name: form_data.name,
            Floor.number: form_data.number,
            Floor.description: form_data.description,
            Floor.coridorCleaningCost: form_data.coridorCleaningCost,
            Floor.branchId: form_data.branchid,
            Floor.type: form_data.type,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
    
