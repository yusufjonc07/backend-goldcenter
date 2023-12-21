from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.branch import *
from app.schemas.branch import *
from app.utils.pagination import pagination


def get_all_branchs(search, page, limit, usr, db: Session):

    branchs = db.query(Branch)

    # if search:
    # branchs = branchs.filter(
    # Branch.id.like(f"%{search}%"),
    # )

    return pagination(branchs, page, limit)


def create_branch(form_data: NewBranch, usr, db: Session):

    try:
        new_branch = Branch(
            name=form_data.name,
            address=form_data.address,
            dollar=form_data.dollar,
        )

        db.add(new_branch)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)


def update_branch(id, form_data: UpdateBranch, usr, db: Session):

    try:
        branch = db.query(Branch).filter(Branch.id == id)
        this_branch = branch.first()
        if this_branch:
            branch.update({
                Branch.name: form_data.name,
                Branch.address: form_data.address,
                Branch.dollar: form_data.dollar,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
