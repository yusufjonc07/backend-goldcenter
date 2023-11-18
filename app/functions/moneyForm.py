import math
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.moneyForm import *
from app.schemas.moneyForm import *
from app.utils.pagination import pagination 

def get_all_moneyForms(search, page, limit, usr, db: Session):
   
    moneyForms = db.query(Moneyform)

    #if search:
       #moneyForms = moneyForms.filter(
           #Moneyform.id.like(f"%{search}%"),
       #)

    return pagination(moneyForms, page, limit)

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
    
