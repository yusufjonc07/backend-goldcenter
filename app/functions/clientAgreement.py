from datetime import date
import math
from sqlalchemy.sql import label, text
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.clientAgreement import *

def get_all_clientAgreements(search, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit



    clientAgreements = db.query(
        label('id', ClientAgreement.id),
        label('clientName', Client.clientName),
        label('shopNumber', Shop.number),
        label('shopArea', Shop.area),
        label('phoneNumber', Client.phoneNumber),
        label('balance', ClientAgreement.balance),
        label('monthlyFee', ClientAgreement.monthlyFee),
        label('nextPaymentDate', ClientAgreement.startedAt),
    ).join(ClientAgreement.client).join(ClientAgreement.shop)

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

    