from datetime import date
from os.path import exists
from fastapi import Body, File, HTTPException, APIRouter, Depends, UploadFile, Query
from typing import Optional, Union

from app.models.user import User
from app.schemas.client import ConfirmFee
from app.schemas.user import NewUser
from app.utils.fileUtil import replace_file, save_file, validate_file
from app.utils.handler import integrityHandler
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.client import *
from app.functions.client import *
from sqlalchemy import func

client_router = APIRouter(tags=['Klient  Endpoint'])


@client_router.get("/clients", description="This router returns list of the clients using pagination")
async def get_clients_list(
    floorId: Optional[int] = 0,
    status: Optional[AgreementStatus] = "active",
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['director', 'accountant', 'clerk']:
        return get_all_clients(floorId, status, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@client_router.get("/client/fees")
def get_client_fees(
    floorId: int = Query(..., ge=1),
    year: int = Query(...),
    month: int = Query(..., le=12),
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if not usr.userRole in ['director', 'accountant']:
        return client_all_fees(floorId, year, month, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@client_router.get("/client/{id}")
async def get_client_one(
    id: int,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        client: Client = db.get(Client, id)
        if client:
            return {
                "id": client.id,
                "inn": client.inn,
                "startedAt": client.startedAt,
                "clientName": client.clientName,
                "chiefName": client.chiefName,
                "liablePerson": client.liablePerson,
                "shopNumber": client.shop.number,
                "shopArea": client.shop.area,
                "phoneNumber": client.phoneNumber,
                "extraPhoneNumber": client.extraPhoneNumber,
                "balance": client.balance,
                "monthlyFee": client.monthlyFee,
                "fileName": client.fileName,
                "type": client.type,
            }
        else:
            raise HTTPException(
                status_code=400, detail="Bunday mijoz mavjud emas!")

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@client_router.post("/client/create")
async def create_new_client(
    clientName: str = Body(...),
    chiefName: str = Body(...),
    phoneNumber: int = Body(...),
    inn: str = Body(...),
    extraPhoneNumber: Optional[int] = Body(0),
    liablePerson: str = Body(..., min_length=5),
    shopId: int = Body(...),
    monthlyFee: float = Body(..., ge=0),
    balance: Optional[float] = Body(0),
    status: Optional[AgreementStatus] = Body('active'),
    startedAt: str = Body(...),
    agreementFile: Union[UploadFile, None, str] = File(None),
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if usr.userRole in ['director', 'accountant']:
        try:

            if agreementFile:
                FileName = await validate_file(agreementFile, ['document'], 3)
            else:
                FileName = None

            shop = db.get(Shop, shopId)
            if not shop:
                raise HTTPException(400, 'Do`kon topilmadi')

            new_client = Client(
                clientName=clientName,
                chiefName=chiefName,
                phoneNumber=phoneNumber,
                inn=inn,
                extraPhoneNumber=extraPhoneNumber if extraPhoneNumber > 0 else None,
                fileName=FileName,
                shopId=shopId,
                monthlyFee=monthlyFee,
                balance=balance,
                status=status,
                type=shop.floor.type,
                startedAt=startedAt,
                liablePerson=liablePerson,
            )

            db.add(new_client)
            db.commit()
            db.refresh(new_client)

            shop.clientId = new_client.id
            db.commit()

            if agreementFile:
                await save_file(agreementFile, FileName, 'clients')

            raise HTTPException(200, "Ma`lumotlar saqlandi!")
        except IntegrityError as e:
            integrityHandler(e)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@client_router.put("/client/{id}/update", description="This router is able to update client")
async def update_one_client(
    id: int,
    liablePerson: str = Body(..., min_length=5),
    shopId: int = Body(...),
    clientName: str = Body(...),
    chiefName: str = Body(...),
    phoneNumber: int = Body(...),
    inn: str = Body(...),
    extraPhoneNumber: int = Body(...),
    monthlyFee: float = Body(..., ge=0),
    balance: float = Body(...),
    status: AgreementStatus = Body(...),
    type: AgreementStatus = Body(...),
    startedAt: date = Body(...),
    File: Optional[UploadFile] = File(None),
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if usr.userRole in ['director', 'accountant']:
        try:
            client = db.query(Client).filter(Client.id == id)
            this_client = client.first()
            if this_client:

                _old_ = this_client

                if File:
                    fileName = await validate_file(File, ['document'], 3)
                else:
                    fileName = this_client.fileName

                client.update({
                    Client.fileName: fileName,
                    Client.shopId: shopId,
                    Client.clientName: clientName,
                    Client.chiefName: chiefName,
                    Client.phoneNumber: phoneNumber,
                    Client.inn: inn,
                    Client.extraPhoneNumber: extraPhoneNumber if extraPhoneNumber > 0 else None,
                    Client.monthlyFee: monthlyFee,
                    Client.balance: balance,
                    Client.status: status,
                    Client.type: type,
                    Client.startedAt: startedAt,
                    Client.liablePerson: liablePerson,
                    Client.closedAt: (func.now() if status ==
                                      'closed' else None)
                })

                db.commit()
                await replace_file(File, _old_.fileName, fileName, 'clients')

                raise HTTPException(
                    status_code=200, detail="O`zgarish saqlandi!")
            else:
                raise HTTPException(
                    status_code=400, detail="So`rovda xatolik!")
        except IntegrityError as e:
            integrityHandler(e)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@client_router.put("/client/fee/confirm")
async def client_fees_comfirmation(
    form_data: ConfirmFee,
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if usr.userRole in ['director', 'accountant']:
        return comfirm_client_fees(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
