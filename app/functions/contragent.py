import math
from sqlalchemy.orm import aliased, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.contragent import *
from app.models.debetHistory import *
from app.models.expense import *
from app.schemas.contragent import *
from app.utils.pagination import pagination
from app.utils.handler import integrityHandler
import calendar


def get_all_contragents(search, page, limit, usr, db: Session):

    contragents = db.query(Contragent)

    # if search:
    # contragents = contragents.filter(
    # Contragent.id.like(f"%{search}%"),
    # )

    return pagination(contragents, page, limit)


def contragent_balance_in_month_subquery(year, month, db, end=True):

    otherDebetHistorys = aliased(DebetHistory)

    if end:
        num_days_in_month = calendar.monthrange(year, month)[1]
    else:
        num_days_in_month = 1

    return (
        Contragent.balance
        -
        db.query(func.coalesce(func.sum(Expense.value), 0)).filter(
            Expense.contragentId == Contragent.id,
            func.date(
                Expense.createdAt) > f"{year}-{month:02d}-{num_days_in_month:02d}",
        ).scalar_subquery()
        +
        db.query(func.coalesce(func.sum(otherDebetHistorys.value), 0)).filter(
            otherDebetHistorys.contragentId == Contragent.id,
            func.date(
                otherDebetHistorys.createdAt) > f"{year}-{month:02d}-{num_days_in_month:02d}",
        ).scalar_subquery()
    )


def create_contragent(form_data: NewContragent, usr, db: Session):

    try:
        new_contragent = Contragent(
            name=form_data.name, categoryId=form_data.categoryId)
        db.add(new_contragent)
        db.commit()
        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise integrityHandler(e)


def update_contragent(id, form_data: UpdateContragent, usr, db: Session):

    try:
        contragent = db.query(Contragent).filter(
            Contragent.id == id)
        this_contragent = contragent.first()
        if this_contragent:
            contragent.update({Contragent.name: form_data.name,
                              Contragent.categoryId: form_data.categoryId})
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise integrityHandler(e)


def delete_contragent(id, usr, db: Session):

    try:

        db.query(Expense).filter_by(contragentId=id).delete()
        db.query(Contragent).filter_by(id=id).delete()
        db.commit()

        raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")

    except IntegrityError as e:
        raise integrityHandler(e)
