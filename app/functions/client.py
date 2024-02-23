from datetime import date
from typing import List
from fastapi import HTTPException
from sqlalchemy.sql import label, func, or_
from sqlalchemy.orm import Session, aliased
from app.models.client import *
from app.models.clientFee import ClientFee
from app.models.floor import Floor
from app.models.income import Income
from app.schemas.client import ConfirmFee
from app.utils.pagination import pagination

import calendar


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
                # electrPrice=client.shop.floor.branch.electrPrice,
                electrPrice=0,
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

    valuePaid = db.query(func.sum(Income.value)).filter(
        Income.forMonth == func.month(ClientFee.createdAt),
        Income.forYear == func.year(ClientFee.createdAt),
        Income.clientId == ClientFee.clientId,
        or_(
            Income.type == 'rent',
            Income.type == 'infrastructure',
        )
    ).subquery()
    electrPaid = db.query(func.sum(Income.value)).filter(
        Income.forMonth == func.month(ClientFee.createdAt),
        Income.forYear == func.year(ClientFee.createdAt),
        Income.clientId == ClientFee.clientId,
        Income.type == 'utility',
    ).subquery()

    query = db.query(
        label('id', ClientFee.id),
        label('clientId', Client.id),
        label('clientName', Client.clientName),
        label('clientType', Client.type),
        label('shopNumber', Shop.number),
        label('shopArea', Shop.area),
        label('value', ClientFee.value),
        label('valuePaid', func.coalesce(valuePaid, 0.0)),
        label('electrPrice', ClientFee.electrPrice),
        label('electrAmount', ClientFee.electrAmount),
        label('electrPaid', func.coalesce(electrPaid, 0.0)),
        label('balance', client_balance_in_month_subquery(year, month, db)),
        label('isConfirmed', ClientFee.isConfirmed),
    )

    return select_fees(query, floorId, year, month)


def client_balance_in_month_subquery(year, month, db, end=True):

    otherClientFees = aliased(ClientFee)

    if end:
        num_days_in_month = calendar.monthrange(year, month)[1]
    else:
        num_days_in_month = 1

    return (
        Client.balance
        -
        db.query(func.coalesce(func.sum(Income.value), 0)).filter(
            Income.clientId == Client.id,
            func.date(
                Income.createdAt) > f"{year}-{month:02d}-{num_days_in_month:02d}",
        ).scalar_subquery()
        +
        db.query(func.coalesce(func.sum(otherClientFees.value+otherClientFees.electrPrice*otherClientFees.electrAmount), 0)).filter(
            otherClientFees.clientId == Client.id,
            otherClientFees.isConfirmed == True,
            func.date(
                otherClientFees.createdAt) > f"{year}-{month:02d}-{num_days_in_month:02d}",
        ).scalar_subquery()
    )


def client_one_fees(id, type, year, month, usr, db: Session):

    valuePaid = db.query(func.sum(Income.value)).filter(
        Income.forMonth == func.month(ClientFee.createdAt),
        Income.forYear == func.year(ClientFee.createdAt),
        Income.clientId == ClientFee.clientId,
        or_(
            Income.type == 'rent',
            Income.type == 'infrastructure',
        )
    ).subquery()
    electrPaid = db.query(func.sum(Income.value)).filter(
        Income.forMonth == func.month(ClientFee.createdAt),
        Income.forYear == func.year(ClientFee.createdAt),
        Income.clientId == ClientFee.clientId,
        Income.type == 'utility',
    ).subquery()

    fee = db.query(
        label('id', ClientFee.id),
        label('clientId', Client.id),
        label('clientName', Client.clientName),
        label('clientType', Client.type),
        label('shopNumber', Shop.number),
        label('shopArea', Shop.area),
        label('value', ClientFee.value),
        label('valuePaid', func.coalesce(valuePaid, 0.0)),
        label('electrPrice', ClientFee.electrPrice),
        label('electrAmount', ClientFee.electrAmount),
        label('electrPaid', func.coalesce(electrPaid, 0.0)),
        label('balance', client_balance_in_month_subquery(year, month, db)),
        label('isConfirmed', ClientFee.isConfirmed),
    ).join(ClientFee.client).join(Client.shop).filter(
        ClientFee.clientId == id,
        func.year(ClientFee.createdAt) == year,
        func.month(ClientFee.createdAt) == month,
    ).first()

    clientBalance = db.query(client_balance_in_month_subquery(
        year, month, db)).filter(Client.id == id).scalar()

    if not fee:
        return {
            "forMonth": 0.0,
            "paidMoney": 0.0,
            "clientBalance": clientBalance,
        }

    print(fee.balance)

    if fee.clientType == 'utility':
        return {
            "forMonth": fee.electrAmount*fee.electrPrice,
            "paidMoney": fee.electrPaid,
            "clientBalance": clientBalance,
        }
    else:
        return {
            "forMonth": fee.value,
            "paidMoney": fee.valuePaid,
            "clientBalance": clientBalance,
        }


def comfirm_client_fees(form_data: ConfirmFee, usr, db: Session):

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
