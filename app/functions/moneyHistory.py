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



def get_all_agreement_payments(clientId, page, limit, usr, db):
   

    incomesData = db.query(
        label("id", Income.id),
        label("value", Income.value),
        label("clientId", Income.clientId),
        label("clientName", Client.clientName),
        label("shopNumber", Shop.number),
        label("liablePerson", Client.liablePerson),
        label("createdAt", Income.createdAt),
        label("moneyForm", Moneyform.name),
        label("comment", Income.comment),
    ).select_from(Income)\
        .join(Income.client)\
        .join(Client.shop).join(Income.moneyForm)\

    if clientId > 0:
        incomesData = incomesData.filter(Income.clientId == clientId)

    # if search:
       # incomesData = incomesData.filter(
        # Income.id.like(f"%{search}%"),
       # )

    return pagination(incomesData, page, limit)
    

