import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.clientAgreement import *
from app.schemas.clientAgreement import *

def get_all_clientAgreements(search, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit
    
    clientAgreements = db.query(ClientAgreement)

    #if search:
       #clientAgreements = clientAgreements.filter(
           #Clientagreement.id.like(f"%{search}%"),
       #)

    
    all_data = clientAgreements.order_by(ClientAgreement.id.desc()).offset(offset).limit(limit)
    count_data = clientAgreements.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }

def create_clientAgreement(form_data: NewClientagreement, usr, db: Session):
    
    try:
        new_clientAgreement = ClientAgreement(
            fileName=form_data.filename,
        shopId=form_data.shopid,
        clientId=form_data.clientid,
        monthlyFee=form_data.monthlyfee,
        balance=form_data.balance,
        status=form_data.status,
    )

        db.add(new_clientAgreement)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)

def update_clientAgreement(id, form_data: UpdateClientagreement, usr, db: Session):
    
    try:
        clientAgreement = db.query(ClientAgreement).filter(ClientAgreement.id == id)
        this_clientAgreement = clientAgreement.first()
        if this_clientAgreement:
            clientAgreement.update({    
            ClientAgreement.fileName: form_data.filename,
            ClientAgreement.shopId: form_data.shopid,
            ClientAgreement.clientId: form_data.clientid,
            ClientAgreement.monthlyFee: form_data.monthlyfee,
            ClientAgreement.balance: form_data.balance,
            ClientAgreement.status: form_data.status,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
    
