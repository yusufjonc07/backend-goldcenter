from datetime import date
from sqlalchemy.sql import label
from sqlalchemy.orm import Session
from app.models.client import *
from app.utils.pagination import pagination

def get_all_clients_with_warehouse(page, limit, usr, db: Session):

    clients = db.query(
        label('id', Client.id),
        label('clientName', Client.clientName),
        label('chiefName', Client.chiefName),
        label('liablePerson', Client.liablePerson),
        label('shopNumber', Shop.number),
        label('phoneNumber', Client.phoneNumber),
        label('placeName', Client.placeName),
        label('placePrice', Client.placePrice),
    ).join(Client.shop).order_by(Shop.number.asc()).filter(Client.placeName!=None)

    return pagination(clients, page, limit)

