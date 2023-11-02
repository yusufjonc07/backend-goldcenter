import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import label
from fastapi import HTTPException
from app.models.client import Client
from app.models.clientAgreement import ClientAgreement
from app.models.moneyHistory import *
from app.models.shop import Shop

def get_all_agreement_payments(id, page, limit, usr, db):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit


    moneyHistorys = db.query(
        label("id", MoneyHistory.id),
        label("value", MoneyHistory.value),
        label("clientName", Client.clientName),
        label("shopNumber", Shop.number),
        label("liablePerson", ClientAgreement.liablePerson),
        label("createdAt", MoneyHistory.createdAt),
        label("moneyForm", Moneyform.name),
        label("comment", MoneyHistory.comment),
    ).select_from(MoneyHistory)\
    .join(ClientAgreement, ClientAgreement.id==MoneyHistory.ownerId)\
    .join(ClientAgreement.client).join(ClientAgreement.shop).join(MoneyHistory.moneyForm)\
    .filter(MoneyHistory.ownerTable == 'clientAgreement')

    if id > 0:
        moneyHistorys = moneyHistorys.filter(MoneyHistory.ownerId==id)

    #if search:
       #moneyHistorys = moneyHistorys.filter(
           #MoneyHistory.id.like(f"%{search}%"),
       #)

    
    all_data = moneyHistorys.order_by(MoneyHistory.createdAt.desc()).offset(offset).limit(limit)
    count_data = moneyHistorys.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }


    

def get_all_moneyHistorys(search, ownerTable, ownerId, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    name = func.IF(
        ownerTable=='clientAgreement',
        db.query(Client.clientName)\
            .select_from(ClientAgreement)\
            .join(ClientAgreement.client)\
            .filter(Client.id==MoneyHistory.ownerId)\
            .subquery(),
        "?"
    )
    
    moneyHistorys = db.query(
        label("name", name),
        label("name", name),
    ).select_from(MoneyHistory)

    #if search:
       #moneyHistorys = moneyHistorys.filter(
           #MoneyHistory.id.like(f"%{search}%"),
       #)

    
    all_data = moneyHistorys.order_by(MoneyHistory.id.desc()).offset(offset).limit(limit)
    count_data = moneyHistorys.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }