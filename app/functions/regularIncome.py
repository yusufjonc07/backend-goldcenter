from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.regularIncome import *
from app.schemas.regularIncome import *
from app.utils.handler import integrityHandler
from app.utils.pagination import pagination


def get_all_regularIncomes(search, page, limit, usr, db: Session):

    regularIncomes = db.query(RegularIncome)

    if search:
        regularIncomes = regularIncomes.filter(
            RegularIncome.name.like(f"%{search}%"),
        )

    return pagination(regularIncomes, page, limit)


def create_regularIncome(form_data: NewRegularincome, usr, db: Session):

    try:
        new_regularIncome = RegularIncome(
            name=form_data.name,
        )

        db.add(new_regularIncome)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        integrityHandler(e)


def update_regularIncome(id, form_data: UpdateRegularincome, usr, db: Session):

    try:
        regularIncome = db.query(RegularIncome).filter(RegularIncome.id == id)
        this_regularIncome = regularIncome.first()
        if this_regularIncome:
            regularIncome.update({
                RegularIncome.name: form_data.name,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
