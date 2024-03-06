import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.income import *
from app.schemas.income import *
from app.utils.handler import integrityHandler
from app.utils.pagination import pagination


def get_all_incomes(search, page, limit, usr, db: Session):

    incomes = db.query(Income)

    # if search:
    # incomes = incomes.filter(
    # Income.id.like(f"%{search}%"),
    # )

    return pagination(incomes, page, limit)


def get_last_electrAmount(id: int, db: Session):
    return db.query(Income).filter_by(
        clientId=id, type='utility'
    ).order_by(Income.electrLastAmount).first()


def create_income(form_data: NewIncome, usr, db: Session):
    try:

        new_income = Income(
            clientId=form_data.clientId if form_data.clientId > 0 else None,
            value=form_data.value,
            moneyFormId=form_data.moneyFormId,
            comment=form_data.comment,
            type=form_data.type,
            forMonth=form_data.forMonth,
            forYear=form_data.forYear,
            userId=usr.id,
        )

        db.add(new_income)
        db.flush()
        db.refresh(new_income)

        if form_data.clientId > 0:
            new_income.client.balance += new_income.value

        new_income.moneyForm.balance += new_income.value

        db.commit()
        raise HTTPException(status_code=200, detail="Ma'lumotlar saqlandi!")

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
                Income.type: form_data.type,
                Income.forMonth: form_data.forMonth,
                Income.forYear: form_data.forYear,
                Income.userId: usr.id,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
