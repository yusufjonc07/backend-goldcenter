from datetime import date
from typing import List
from fastapi import HTTPException
from sqlalchemy.sql import label, func
from sqlalchemy.orm import Session
from app.models.client import *
from app.models.clientFee import ClientFee
from app.models.floor import Floor
from app.schemas.client import ConfirmFee
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
        .filter(Client.status == status)

    if floorId > 0:
        clients = clients.filter(Shop.floorId == floorId)

    clients = clients.order_by(Shop.number.asc())

    return pagination(clients, page, limit)


def check_and_create(year, month, usr, db: Session):
    clients = db.query(Client).join(Client.shop).join(Shop.floor).filter(
        Floor.branchId == usr.employee.branchId
    ).all()
    for client in clients:
        fee = db.query(ClientFee).filter(
            ClientFee.clientId == client.id,
            func.year(ClientFee.createdAt) == year,
            func.month(ClientFee.createdAt) == month,
        ).first()

        if fee is None:
            db.add(ClientFee(
                clientId=client.id,
                value=client.monthlyFee if client.shop.floor.type == 'rent' else client.shop.area *
                client.monthlyFee,
                electrPrice=client.shop.floor.branch.electrPrice,
                createdAt=date(year, month, 1),
            ))
    db.commit()
    return


def select_fees(query: Session, floorId, year, month):
    return query.join(ClientFee.client).join(Client.shop).filter(
        Shop.floorId == floorId,
        func.year(ClientFee.createdAt) == year,
        func.month(ClientFee.createdAt) == month,
    ).group_by(ClientFee.id).all()


def client_all_fees(floorId, year, month, usr, db: Session):

    check_and_create(year, month, usr, db)

    floor: Floor = db.get(Floor, floorId)

    if not floor:
        raise HTTPException(400, 'Qavat topilmadi!')

    # if :
    #     calcFee = Client.monthlyFee
    # else:
    #     calcFee = Client.monthlyFee * Shop.area

    query = db.query(
        label('id', ClientFee.id),
        label('clientId', Client.id),
        label('clientName', Client.clientName),
        label('clientType', Client.type),
        label('shopNumber', Shop.number),
        label('shopArea', Shop.area),
        label('value', ClientFee.value),
        label('valuePaid', 1000.0),
        label('electrPrice', ClientFee.electrPrice),
        label('electrAmount', ClientFee.electrAmount),
        label('electrPaid', 1000.0),
        label('balance', Client.balance),
        label('isConfirmed', ClientFee.isConfirmed),
    )

    return select_fees(query, floorId, year, month)


def comfirm_client_fees(form_data: ConfirmFee, usr, db: Session):

    floor: Floor = db.get(Floor, form_data.floorId)

    if not floor:
        raise HTTPException(400, 'Qavat topilmadi!')

    clientFee = db.query(ClientFee).filter(
        ClientFee.id == form_data.clientFeeId
    ).first()

    if not clientFee:
        raise HTTPException(400, 'Ma`lumot topilmadi!')

    if clientFee.isConfirmed == True:
        clientFee.client.balance += (clientFee.value +
                                     (clientFee.electrPrice*clientFee.electrAmount))

    clientFee.value = form_data.value
    clientFee.electrPrice = form_data.electrPrice
    clientFee.electrAmount = form_data.electrAmount

    clientFee.client.balance -= (clientFee.value +
                                 (clientFee.electrPrice*clientFee.electrAmount))
    clientFee.isConfirmed = True

    db.commit()
    raise HTTPException(200, 'Ma\'lumotlar saqlandi!')
