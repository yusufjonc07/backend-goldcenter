import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.shop import *
from app.schemas.shop import *
from app.utils.handler import integrityHandler

def get_all_shops(floorId, search, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit
    
    shops = db.query(Shop)

    if floorId > 0:
        shops = shops.filter(Shop.floorId==floorId)

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

def divide_shop(shopId:int, db: Session):
    shop: Shop = db.query(Shop, shopId)
    newShop = Shop(
        name=f"{shop.name}.b",
        number=f"{shop.number}.b",
        floorId=shop.floorId,
        area=shop.area
    )

    if shop.boxHeight > shop.boxWith:
        shop.boxHeight /= 2
        
#         fromTop
# fromLeft
# boxWith
# boxHeight


    else:
        shop.boxWith /= 2


    shop.number += ".a"
    shop.name += ".a"


def create_shop(form_data: NewShop, usr, db: Session):
    
    try:

        new_shop = Shop(
            name=form_data.name,
            number=form_data.number,
            floorId=form_data.floorId,
            area=form_data.area,
            fromTop=form_data.fromTop,
            fromLeft=form_data.fromLeft,
            boxWith=form_data.boxWith,
            boxHeight=form_data.boxHeight,
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
                Shop.fromTop: form_data.fromTop,
                Shop.fromLeft: form_data.fromLeft,
                Shop.boxWith: form_data.boxWith,
                Shop.boxHeight: form_data.boxHeight,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise integrityHandler(e)
    
