import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.shop import *
from app.schemas.shop import *
from app.utils.handler import integrityHandler

def get_all_shops(search, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit
    
    shops = db.query(Shop)

    #if search:
       #shops = shops.filter(
           #Shop.id.like(f"%{search}%"),
       #)

    
    all_data = shops.order_by(Shop.id.desc()).offset(offset).limit(limit)
    count_data = shops.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }

def create_shop(form_data: NewShop, usr, db: Session):
    
    try:
        new_shop = Shop(
            name=form_data.name,
            number=form_data.number,
            floorId=form_data.floorId,
            area=form_data.area,
        )

        db.add(new_shop)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise integrityHandler(e)

def update_shop(id, form_data: UpdateShop, usr, db: Session):
    
    try:
        shop = db.query(Shop).filter(Shop.id == id)
        this_shop = shop.first()
        if this_shop:
            shop.update({    
                Shop.name: form_data.name,
                Shop.number: form_data.number,
                Shop.floorId: form_data.floorId,
                Shop.area: form_data.area,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise integrityHandler(e)
    
