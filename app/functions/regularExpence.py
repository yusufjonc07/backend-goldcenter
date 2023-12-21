import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.regularExpence import *
from app.schemas.regularExpence import *
from app.utils.pagination import pagination


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
        raise HTTPException(400, e.args)


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
        raise HTTPException(400, e.args)
