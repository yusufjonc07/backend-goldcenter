import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.regularExpence import *
from app.models.expense import *
from app.schemas.regularExpence import *
from app.utils.pagination import pagination
from app.utils.handler import integrityHandler


def get_all_regularExpences(search, page, limit, usr, db: Session):

    regularExpences = db.query(Regularexpence)

    # if search:
    # regularExpences = regularExpences.filter(
    # Regularexpence.id.like(f"%{search}%"),
    # )

    return pagination(regularExpences, page, limit)


def create_regularExpence(form_data: NewRegularexpence, usr, db: Session):

    try:
        new_regularExpence = Regularexpence(name=form_data.name)
        db.add(new_regularExpence)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise integrityHandler(e)


def update_regularExpence(id, form_data: UpdateRegularexpence, usr, db: Session):

    try:
        regularExpence = db.query(Regularexpence).filter(
            Regularexpence.id == id)
        this_regularExpence = regularExpence.first()
        if this_regularExpence:
            regularExpence.update({Regularexpence.name: form_data.name})
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise integrityHandler(e)


def delete_regularExpence(id, usr, db: Session):

    try:

        db.query(Expense).filter_by(regularExpenceId=id).delete()
        db.query(Regularexpence).filter_by(id=id).delete()
        db.commit()

        raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")

    except IntegrityError as e:
        raise integrityHandler(e)
