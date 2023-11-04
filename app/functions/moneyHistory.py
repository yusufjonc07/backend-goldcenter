import math
from sqlalchemy.orm import joinedload, Session, aliased
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import label
from fastapi import HTTPException
from app.models.client import Client
from app.models.clientAgreement import ClientAgreement
from app.models.expense import *
from app.models.income import *
from app.models.shop import Shop


def get_all_agreement_payments(id, page, limit, usr, db):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    incomesData = db.query(
        label("id", Income.id),
        label("value", Income.value),
        label("clientName", Client.clientName),
        label("shopNumber", Shop.number),
        label("liablePerson", ClientAgreement.liablePerson),
        label("createdAt", Income.createdAt),
        label("moneyForm", Moneyform.name),
        label("comment", Income.comment),
    ).select_from(Income)\
        .join(Income.clientAgreement).join(ClientAgreement.client)\
        .join(ClientAgreement.shop).join(Income.moneyForm)\

    if id > 0:
        incomesData = incomesData.filter(Income.clientAgreementId == id)

    # if search:
       # incomesData = incomesData.filter(
        # Income.id.like(f"%{search}%"),
       # )

    all_data = incomesData.order_by(
        Income.createdAt.desc()).offset(offset).limit(limit)
    count_data = incomesData.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }


