from datetime import date
import math
from sqlalchemy.sql import label, text
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.client import *

def get_all_clients(floorId, status, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit


    clients = db.query(
        label('id', Client.id),
        label('clientName', Client.clientName),
        label('chiefName', Client.chiefName),
        label('liablePerson', Client.liablePerson),
        label('shopNumber', Shop.number),
        label('shopArea', Shop.area),
        label('phoneNumber', Client.phoneNumber),
        label('balance', Client.balance),
        label('monthlyFee', Client.monthlyFee),
        label('nextPaymentDate', Client.startedAt),
    ).join(Client.shop)\
    .filter(Client.status==status)

    if floorId > 0:
        clients = clients.filter(Shop.floorId==floorId)

    #if search:
       #clients = clients.filter(
           #Client.id.like(f"%{search}%"),
       #)
    all_data = clients.order_by(Shop.number.asc()).offset(offset).limit(limit)
    count_data = clients.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }

    