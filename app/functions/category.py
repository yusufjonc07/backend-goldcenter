from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.category import *
from app.schemas.category import *
from app.utils.handler import integrityHandler
from app.utils.pagination import pagination


def get_all_categorys(search, type, page, limit, usr, db: Session):

    categorys = db.query(Category)

    if type:
        categorys = categorys.filter(Category.type == type)

    if search:
        categorys = categorys.filter(
            Category.name.like(f"%{search}%"),
        )

    return pagination(categorys, page, limit)


def create_category(form_data: NewCategory, usr, db: Session):

    try:
        new_category = Category(
            name=form_data.name,
            type=form_data.type,
        )

        db.add(new_category)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        integrityHandler(e)


def update_category(id, form_data: UpdateCategory, usr, db: Session):

    try:
        category = db.query(Category).filter(Category.id == id)
        this_category = category.first()
        if this_category:
            category.update({
                Category.name: form_data.name,
                Category.type: form_data.type,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
