import math
from sqlalchemy.orm import aliased, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.regularExpence import *
from app.models.debetHistory import *
from app.models.expense import *
from app.schemas.regularExpence import *
from app.utils.pagination import pagination
from app.utils.handler import integrityHandler
import calendar


def get_all_regularExpences(search, page, limit, usr, db: Session):

    regularExpences = db.query(RegularExpence)

    # if search:
    # regularExpences = regularExpences.filter(
    # RegularExpence.id.like(f"%{search}%"),
    # )

    return pagination(regularExpences, page, limit)


def regularExpence_balance_in_month_subquery(year, month, db, end=True):

    otherDebetHistorys = aliased(DebetHistory)

    if end:
        num_days_in_month = calendar.monthrange(year, month)[1]
    else:
        num_days_in_month = 1

    return (
        RegularExpence.balance
        -
        db.query(func.coalesce(func.sum(Expense.value), 0)).filter(
            Expense.regularExpenceId == RegularExpence.id,
            func.date(
                Expense.createdAt) > f"{year}-{month:02d}-{num_days_in_month:02d}",
        ).scalar_subquery()
        +
        db.query(func.coalesce(func.sum(otherDebetHistorys.value), 0)).filter(
            otherDebetHistorys.regularExpenceId == RegularExpence.id,
            func.date(
                otherDebetHistorys.createdAt) > f"{year}-{month:02d}-{num_days_in_month:02d}",
        ).scalar_subquery()
    )


def create_regularExpence(form_data: NewRegularexpence, usr, db: Session):

    try:
        new_regularExpence = RegularExpence(name=form_data.name)
        db.add(new_regularExpence)
        db.commit()
        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise integrityHandler(e)


def update_regularExpence(id, form_data: UpdateRegularexpence, usr, db: Session):

    try:
        regularExpence = db.query(RegularExpence).filter(
            RegularExpence.id == id)
        this_regularExpence = regularExpence.first()
        if this_regularExpence:
            regularExpence.update({RegularExpence.name: form_data.name})
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise integrityHandler(e)


def delete_regularExpence(id, usr, db: Session):

    try:

        db.query(Expense).filter_by(regularExpenceId=id).delete()
        db.query(RegularExpence).filter_by(id=id).delete()
        db.commit()

        raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")

    except IntegrityError as e:
        raise integrityHandler(e)
