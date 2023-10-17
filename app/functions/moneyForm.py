import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.moneyForm import *
from app.schemas.moneyForm import *

def get_all_moneyForms(search, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit
    
    moneyForms = db.query(Moneyform)

    #if search:
       #moneyForms = moneyForms.filter(
           #Moneyform.id.like(f"%{search}%"),
       #)

    
    all_data = moneyForms.order_by(Moneyform.id.desc()).offset(offset).limit(limit)
    count_data = moneyForms.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }

def create_moneyForm(form_data: NewMoneyform, usr, db: Session):
    
    try:
        new_moneyForm = Moneyform(
            name=form_data.name,
    )

        db.add(new_moneyForm)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)

def update_moneyForm(id, form_data: UpdateMoneyform, usr, db: Session):
    
    try:
        moneyForm = db.query(Moneyform).filter(Moneyform.id == id)
        this_moneyForm = moneyForm.first()
        if this_moneyForm:
            moneyForm.update({    
            Moneyform.name: form_data.name,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
    
