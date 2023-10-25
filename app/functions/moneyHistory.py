import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import label
from fastapi import HTTPException
from app.models.client import Client
from app.models.clientAgreement import ClientAgreement
from app.models.moneyHistory import *

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
        label("name", )
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