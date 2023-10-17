import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.regularExpence import *
from app.schemas.regularExpence import *

def get_all_regularExpences(search, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit
    
    regularExpences = db.query(Regularexpence)

    #if search:
       #regularExpences = regularExpences.filter(
           #Regularexpence.id.like(f"%{search}%"),
       #)

    
    all_data = regularExpences.order_by(Regularexpence.id.desc()).offset(offset).limit(limit)
    count_data = regularExpences.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }

def create_regularExpence(form_data: NewRegularexpence, usr, db: Session):
    
    try:
        new_regularExpence = Regularexpence(
            name=form_data.name,
        floorId=form_data.floorid,
        branchId=form_data.branchid,
        addingToFee=form_data.addingtofee,
    )

        db.add(new_regularExpence)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)

def update_regularExpence(id, form_data: UpdateRegularexpence, usr, db: Session):
    
    try:
        regularExpence = db.query(Regularexpence).filter(Regularexpence.id == id)
        this_regularExpence = regularExpence.first()
        if this_regularExpence:
            regularExpence.update({    
            Regularexpence.name: form_data.name,
            Regularexpence.floorId: form_data.floorid,
            Regularexpence.branchId: form_data.branchid,
            Regularexpence.addingToFee: form_data.addingtofee,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
    
