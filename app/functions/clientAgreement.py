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

    _current_month = func.MONTH(func.now())
    _current_year = func.YEAR(func.now())
    _aggDate = func.DAY(ClientAgreement.startedAt)
    _aggDateR = func.IF(_aggDate < 10, func.CONCAT('0', _aggDate), _aggDate)

    _caseThisMonth = func.CONCAT(
        _current_year, '-', 
        func.IF(_current_month < 10, func.CONCAT('0', _current_month), _current_month), '-', 
        _aggDateR,
    )
    
    _caseNextMonth = func.CONCAT(_current_year, '-', _current_month+1, '-', _aggDateR)
    _caseNextYear = func.CONCAT(_current_year+1, '-01-', _aggDateR)

    _next_payment_date = func.IF(
        func.DAY(ClientAgreement.startedAt) < func.DAY(func.now()), 
        func.IF(_current_month == 12, _caseNextYear, _caseNextMonth),
        _caseThisMonth
    )
    
    clientAgreements = db.query(
        label('id', ClientAgreement.id),
        label('clientName', Client.clientName),
        label('shopNumber', Shop.number),
        label('shopArea', Shop.area),
        label('phoneNumber', Client.phoneNumber),
        label('balance', ClientAgreement.balance),
        label('monthlyFee', ClientAgreement.monthlyFee),
        label('nextPaymentDate', _next_payment_date),
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

    