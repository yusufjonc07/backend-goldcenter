import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.moneyHistory import *
from app.schemas.moneyHistory import *

def get_all_moneyHistorys(search, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit
    
    moneyHistorys = db.query(Moneyhistory)

    #if search:
       #moneyHistorys = moneyHistorys.filter(
           #Moneyhistory.id.like(f"%{search}%"),
       #)

    
    all_data = moneyHistorys.order_by(Moneyhistory.id.desc()).offset(offset).limit(limit)
    count_data = moneyHistorys.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }

def create_moneyHistory(form_data: NewMoneyhistory, usr, db: Session):
    
    try:
        new_moneyHistory = Moneyhistory(
            ownerTable=form_data.ownertable,
        ownerId=form_data.ownerid,
        value=form_data.value,
        moneyFormId=form_data.moneyformid,
        branchId=form_data.branchid,
        comment=form_data.comment,
        userId=form_data.userid,
        fileName=form_data.filename,
        createdAt=form_data.createdat,
    )

        db.add(new_moneyHistory)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)

def update_moneyHistory(id, form_data: UpdateMoneyhistory, usr, db: Session):
    
    try:
        moneyHistory = db.query(Moneyhistory).filter(Moneyhistory.id == id)
        this_moneyHistory = moneyHistory.first()
        if this_moneyHistory:
            moneyHistory.update({    
            Moneyhistory.ownerTable: form_data.ownertable,
            Moneyhistory.ownerId: form_data.ownerid,
            Moneyhistory.value: form_data.value,
            Moneyhistory.moneyFormId: form_data.moneyformid,
            Moneyhistory.branchId: form_data.branchid,
            Moneyhistory.comment: form_data.comment,
            Moneyhistory.userId: form_data.userid,
            Moneyhistory.fileName: form_data.filename,
            Moneyhistory.createdAt: form_data.createdat,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
    
