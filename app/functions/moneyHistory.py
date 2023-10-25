import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.moneyHistory import *

def get_all_moneyHistorys(search, ownerTable, ownerId, page, limit, usr, db: Session):
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