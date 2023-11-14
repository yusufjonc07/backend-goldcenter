import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.income import *
from app.schemas.income import *
from app.utils.handler import integrityHandler


def get_all_incomes(search, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    incomes = db.query(Income)

    # if search:
    # incomes = incomes.filter(
    # Income.id.like(f"%{search}%"),
    # )

    all_data = incomes.order_by(Income.id.desc()).offset(offset).limit(limit)
    count_data = incomes.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }


def create_income(form_data: NewIncome, usr, db: Session):

    try:
        new_income = Income(
            clientId=form_data.clientId,
            value=form_data.value,
            moneyFormId=form_data.moneyFormId,
            comment=form_data.comment,
            userId=usr.id,
        )

        db.add(new_income)
        db.flush()
        db.refresh(new_income)
        new_income.client.balance += new_income.value
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise integrityHandler(e)


def update_income(id, form_data: UpdateIncome, usr, db: Session):

    try:
        income = db.query(Income).filter(Income.id == id)
        this_income = income.first()
        if this_income:
            income.update({
                Income.clientId: form_data.clientId,
                Income.value: form_data.value,
                Income.moneyFormId: form_data.moneyFormId,
                Income.comment: form_data.comment,
                Income.userId: usr.id,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
