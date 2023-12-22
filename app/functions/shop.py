import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.shop import *
from app.schemas.shop import *
from app.utils.handler import integrityHandler
from app.utils.pagination import pagination


def get_all_shops(floorId, search, page, limit, usr, db: Session):

    shops = db.query(Shop).filter(Shop.deleted == False)

    if floorId > 0:
        shops = shops.filter(Shop.floorId == floorId)

    # if search:
       # shops = shops.filter(
        # Shop.id.like(f"%{search}%"),
       # )

    return pagination(shops, page, limit)


def combine_shop(form_data: CombineShops, db: Session):
    mainShop: Shop = db.get(Shop, form_data.mainShopId)
    deletingShop: Shop = db.get(Shop, form_data.deletingShopId)

    if deletingShop.clientId > 0:
        raise HTTPException(
            400, 'Bu do`konni qo`shib yuborishdan oldin undagi shartnomani yakunlang!')


def divide_shop(form_data: DivideShop, db: Session):

    SHOPS_GAP = 1

    try:
        shop: Shop = db.query(Shop).filter_by(id=form_data.shopId).first()
        newShop = Shop(
            name=f"{shop.name}.b",
            number=f"{shop.number}.b",
            floorId=shop.floorId,
            area=shop.area
        )

        if shop.boxHeight > shop.boxWith:
            shop.boxHeight /= 2
            newShop.fromLeft = shop.fromLeft
            newShop.fromTop = shop.fromTop + shop.boxHeight + SHOPS_GAP
            newShop.boxWith = shop.boxWith
            newShop.boxHeight = shop.boxHeight
        else:
            shop.boxWith /= 2
            newShop.fromTop = shop.fromTop
            newShop.fromLeft = shop.fromLeft + shop.boxWith + SHOPS_GAP
            newShop.boxWith = shop.boxWith
            newShop.boxHeight = shop.boxHeight

        shop.number += ".a"
        shop.name += ".a"
        shop.area = form_data.areaA
        newShop.area = form_data.areaB
        db.add(newShop)
        db.commit()
        return HTTPException(200, 'Xona 2 ga bo`lindi!')

    except Exception as e:
        integrityHandler(e)


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
