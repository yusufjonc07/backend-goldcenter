from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.models.clientAgreement import ClientAgreement
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.shop import *
from app.functions.shop import *
from app.schemas.shop import *

shop_router = APIRouter(tags=['Shop Endpoint'])

@shop_router.get("/shops", description="This router returns list of the shops using pagination")
async def get_shops_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_all_shops(search, page, limit, usr, db)  
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")  

@shop_router.post("/shop/create", description="This router is able to add new shop")
async def create_new_shop(
    form_data: NewShop,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_shop(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@shop_router.get("/shop/detail")
async def shop_view(
    shop_id: int,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return db.query(Shop).options(
            joinedload(Shop.clientAgreement.and_(ClientAgreement.clientId==Shop.clientId))
        ).filter(Shop.id==shop_id).first()
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@shop_router.put("/shop/{id}/update", description="This router is able to update shop")
async def update_one_shop(
    id: int,
    form_data: UpdateShop,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_shop(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
