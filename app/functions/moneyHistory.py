import math
from sqlalchemy.orm import joinedload, Session, aliased
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
        .join(ClientAgreement, ClientAgreement.id == MoneyHistory.ownerId)\
        .join(ClientAgreement.client).join(ClientAgreement.shop).join(MoneyHistory.moneyForm)\
        .filter(MoneyHistory.ownerTable == 'clientAgreement')

    if id > 0:
        moneyHistorys = moneyHistorys.filter(MoneyHistory.ownerId == id)

    # if search:
       # moneyHistorys = moneyHistorys.filter(
        # MoneyHistory.id.like(f"%{search}%"),
       # )

    all_data = moneyHistorys.order_by(
        MoneyHistory.createdAt.desc()).offset(offset).limit(limit)
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
        MoneyHistory.ownerTable == 'clientAgreement',
        db.query(Client.clientName)
        .join(ClientAgreement.client)
        .filter(Client.id == MoneyHistory.ownerId)
        .subquery(),
        func.IF(MoneyHistory.ownerTable == 'employee', db.query(func.concat(Employee.firstname, ' ', Employee.lastname))
                .select_from(Employee)
                .filter(Employee.id == MoneyHistory.ownerId)
                .subquery(),  "?")
    )

    moneyHistorys = db.query(
        label("ownerTable", MoneyHistory.ownerTable),
        label("given", name),
        label("liablePerson", func.concat(Employee.firstname, ' ', Employee.lastname)),
        label("createdAt", MoneyHistory.createdAt),
        label("value", MoneyHistory.value),
        label("moneyForm", Moneyform.name),
    ).select_from(MoneyHistory).join(MoneyHistory.user).join(User.employee).join(MoneyHistory.moneyForm)

    # if search:
    # moneyHistorys = moneyHistorys.filter(
    # MoneyHistory.id.like(f"%{search}%"),
    # )

    all_data = moneyHistorys.order_by(
        MoneyHistory.id.desc()).offset(offset).limit(limit)
    count_data = moneyHistorys.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }


def get_all_wages(search, ownerId, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit
    
    worker_alias = aliased(Employee, name='worker_alias')
    

    moneyHistorys = db.query(
        label("ownerTable", MoneyHistory.ownerTable),
        label("given", func.concat(worker_alias.firstname, ' ', worker_alias.lastname)),
        label("liablePerson", func.concat(Employee.firstname, ' ', Employee.lastname)),
        label("createdAt", MoneyHistory.createdAt),
        label("value", MoneyHistory.value),
        label("moneyForm", Moneyform.name),
    ).select_from(MoneyHistory)\
        .filter(MoneyHistory.ownerTable=='employee')\
        .join(MoneyHistory.user).join(User.employee)\
        .join(MoneyHistory.moneyForm).join(worker_alias, worker_alias.id==MoneyHistory.ownerId)

    # if search:
    # moneyHistorys = moneyHistorys.filter(
    # MoneyHistory.id.like(f"%{search}%"),
    # )

    all_data = moneyHistorys.order_by(
        MoneyHistory.id.desc()).offset(offset).limit(limit)
    count_data = moneyHistorys.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }
