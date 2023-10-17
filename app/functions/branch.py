import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.branch import *
from app.schemas.branch import *

def get_all_branchs(search, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit
    
    branchs = db.query(Branch)

    #if search:
       #branchs = branchs.filter(
           #Branch.id.like(f"%{search}%"),
       #)

    
    all_data = branchs.order_by(Branch.id.desc()).offset(offset).limit(limit)
    count_data = branchs.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }

def create_branch(form_data: NewBranch, usr, db: Session):
    
    try:
        new_branch = Branch(
            name=form_data.name,
        address=form_data.address,
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
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
    
