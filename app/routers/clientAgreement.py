from datetime import date
from os.path import exists
import os
import uuid
from fastapi import Body, File, HTTPException, APIRouter, Depends, UploadFile
from typing import Optional
from app.functions.moneyHistory import get_all_agreement_payments
from app.models.user import User
from app.schemas.user import NewUser
from app.utils.fileUtil import replace_file, save_file, validate_file
from app.utils.handler import integrityHandler
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import Session
from app.models.clientAgreement import *
from app.functions.clientAgreement import *

clientAgreement_router = APIRouter(tags=['Clientagreement Endpoint'])

@clientAgreement_router.get("/clientAgreements", description="This router returns list of the clientAgreements using pagination")
async def get_clientAgreements_list(
    # search: Optional[str] = "",
    floorId: int,
    status: Optional[AgreementStatus] = "active",
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_all_clientAgreements(floorId, status, page, limit, usr, db)  
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")  
    

@clientAgreement_router.get("/clientAgreement/payments")
async def get_agreement_payments(
    id: Optional[int] = 0,
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_agreement_payments(id, page, limit, usr, db)  
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@clientAgreement_router.post("/clientAgreement/create", description="This router is able to add new clientAgreement")
async def create_new_clientAgreement(
    liablePerson: str = Body(..., min_length=5),
    shopId: int = Body(...),
    clientId: str = Body(...),
    monthlyFee: float = Body(..., ge=0),
    balance: float = Body(...),
    status: AgreementStatus = Body(...),
    type: AgreementType = Body(...),
    startedAt: date = Body(...),
    agreementFile: UploadFile = File(...),
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        try:

            agreementFileName = await validate_file(agreementFile, ['document'], 3)

            new_clientAgreement = ClientAgreement(
                fileName=agreementFileName,
                shopId=shopId,
                clientId=clientId,
                monthlyFee=monthlyFee,
                balance=balance,
                status=status,
                type=type,
                startedAt=startedAt,
                liablePerson=liablePerson,
            )

            db.add(new_clientAgreement)
            db.commit()

            await save_file(agreementFile, agreementFileName, 'clientAgreements')

            raise HTTPException(200, "Ma`lumotlar saqlandi!")
        except IntegrityError as e:
            raise integrityHandler(e)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@clientAgreement_router.put("/clientAgreement/{id}/update", description="This router is able to update clientAgreement")
async def update_one_clientAgreement(
    id: int,
    liablePerson: str = Body(..., min_length=5),
    shopId: int = Body(...),
    clientId: str = Body(...),
    monthlyFee: float = Body(..., ge=0),
    balance: float = Body(...),
    status: AgreementStatus = Body(...),
    type: AgreementType = Body(...),
    startedAt: date = Body(...),
    agreementFile: Optional[UploadFile] = File(None),
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        try:
            clientAgreement = db.query(ClientAgreement).filter(ClientAgreement.id == id)
            this_clientAgreement = clientAgreement.first()
            if this_clientAgreement:

                _old_agreement = this_clientAgreement

                if agreementFile:
                    fileName = await validate_file(agreementFile, ['document'], 3)
                else:
                    fileName = this_clientAgreement.fileName

                clientAgreement.update({
                    ClientAgreement.fileName: fileName,
                    ClientAgreement.shopId: shopId,
                    ClientAgreement.clientId: clientId,
                    ClientAgreement.monthlyFee: monthlyFee,
                    ClientAgreement.balance: balance,
                    ClientAgreement.status: status,
                    ClientAgreement.type: type,
                    ClientAgreement.startedAt: startedAt,
                    ClientAgreement.liablePerson: liablePerson,
                    ClientAgreement.closedAt: (func.now() if status == 'closed' else None)
                })
                db.commit()
                await replace_file(agreementFile, _old_agreement.fileName, fileName, 'clientAgreements')


                raise HTTPException(
                    status_code=200, detail="O`zgarish saqlandi!")
            else:
                raise HTTPException(
                    status_code=400, detail="So`rovda xatolik!")
        except IntegrityError as e:
            integrityHandler(e)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
