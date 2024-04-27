import math
from sqlalchemy.orm import joinedload, Session, aliased
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import label
from fastapi import HTTPException
from app.models.client import Client
from app.models.expense import *
from app.models.income import *
from app.models.shop import Shop
from app.utils.pagination import pagination


def get_all_agreement_payments(moneyFormId, clientId, regularIncomeId, floorId, type, fromDate, toDate, page, limit, usr, db):

    incomesData = db.query(
        label("id", Income.id),
        label("value", Income.value),
        label("clientId", Income.clientId),
        label("clientName", Client.clientName),
        label("regularIncomeId", Income.regularIncomeId),
        label("regularIncomeName", RegularIncome.name),
        label("shopNumber", Shop.number),
        label("liablePerson", Client.liablePerson),
        label("createdAt", Income.createdAt),
        label("moneyForm", Moneyform.name),
        label("comment", Income.comment),
        label("employeeName", Employee._fullname),
    ).select_from(Income)\
        .outerjoin(Client, Income.clientId == Client.id)\
        .outerjoin(Shop, Income.clientId == Shop.id)\
        .outerjoin(RegularIncome, Income.regularIncomeId == RegularIncome.id)\
        .join(Income.user)\
        .join(User.employee)\
        .join(Income.moneyForm)

    if type:
        incomesData = incomesData.filter(Income.type == type)

    if clientId > 0:
        incomesData = incomesData.filter(Income.clientId == clientId)

    if regularIncomeId > 0:
        incomesData = incomesData.filter(
            Income.regularIncomeId == regularIncomeId)

    if moneyFormId > 0:
        incomesData = incomesData.filter(Income.moneyFormId == moneyFormId)

    if floorId > 0:
        incomesData = incomesData.filter(Shop.floorId == floorId)

    if fromDate and toDate:
        incomesData = incomesData.filter(
            func.date(Income.createdAt) >= fromDate,
            func.date(Income.createdAt) <= toDate,
        )

    

    # if search:
    # incomesData = incomesData.filter(
    # Income.id.like(f"%{search}%"),
    # )

    incomesData = incomesData.order_by(Income.createdAt.desc())

    return pagination(incomesData, page, limit)
