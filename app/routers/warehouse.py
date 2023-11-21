from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.functions.warehouse import get_all_clients_with_warehouse
from app.models.client import Client
from app.models.user import User
from app.schemas.client import FormWarehouseClient
from app.utils.handler import integrityHandler
from databases.main import ActiveSession
from app.schemas.user import NewUser
from sqlalchemy.sql import label
from security.auth import get_current_active_user
from sqlalchemy.exc import IntegrityError

warehouse_router = APIRouter(tags=['Ombor bo`limi'], prefix='/warehouse')


@warehouse_router.get("/clients")
async def clients(
    page: Optional[int] = 1,
    limit: Optional[int] = 25,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_clients_with_warehouse(page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
    



@warehouse_router.post("/add_client/{id}")
async def add_one_client(
    id: int,
    form_data: FormWarehouseClient,
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        try:
            client = db.query(Client).filter(Client.id == id).first()
            if client:

                client.placeName=form_data.placeName
                client.placePrice=form_data.placePrice

                db.commit()

                raise HTTPException(
                    status_code=200, detail="O`zgarish saqlandi!")
            else:
                raise HTTPException(
                    status_code=400, detail="So`rovda xatolik!")
        except IntegrityError as e:
            integrityHandler(e)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@warehouse_router.delete("/delete_client/{id}")
async def delete_one_client(
    id: int,
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        try:
            client = db.query(Client).filter(Client.id == id).first()
            if client:

                client.placeName=None
                client.placePrice=None

                db.commit()

                raise HTTPException(
                    status_code=200, detail="Mijoz ombor foydalanuvchilari ro'yxatidan o'chirildi!")
            else:
                raise HTTPException(
                    status_code=400, detail="So`rovda xatolik!")
        except IntegrityError as e:
            integrityHandler(e)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
