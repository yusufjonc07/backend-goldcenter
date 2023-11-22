from datetime import date
from sqlalchemy.sql import label
from sqlalchemy.orm import Session
from app.models.client import *
from app.utils.pagination import pagination

def get_all_clients(floorId, status, page, limit, usr, db: Session):

    clients = db.query(
        label('id', Client.id),
        label('inn', Client.inn),
        label('startedAt', Client.startedAt),
        label('clientName', Client.clientName),
        label('chiefName', Client.chiefName),
        label('liablePerson', Client.liablePerson),
        label('shopNumber', Shop.number),
        label('shopArea', Shop.area),
        label('phoneNumber', Client.phoneNumber),
        label('balance', Client.balance),
        label('monthlyFee', Client.monthlyFee),
        label('fileName', Client.fileName),
        label('type', Client.type),
    ).join(Client.shop)\
    .filter(Client.status==status)

    if floorId > 0:
        clients = clients.filter(Shop.floorId==floorId)

    clients = clients.order_by(Shop.number.asc())

    return pagination(clients, page, limit)

