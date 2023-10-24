from datetime import date
from os.path import exists
import os
import uuid
from fastapi import Body, File, HTTPException, APIRouter, Depends, UploadFile
from typing import Optional
from app.models.user import User
from app.routers.employee import CONTENT_TYPE_LOOKUP_TABLE
from app.schemas.user import NewUser
from app.utils.handler import integrityHandler
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import Session
from app.models.clientAgreement import *
from app.functions.clientAgreement import *

clientAgreement_router = APIRouter(tags=['Clientagreement Endpoint'])

@clientAgreement_router.get("/clientAgreements", description="This router returns list of the clientAgreements using pagination")
async def get_clientAgreements_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_all_clientAgreements(search, page, limit, usr, db)  
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

            if not agreementFile.content_type in CONTENT_TYPE_LOOKUP_TABLE:
                raise HTTPException(
                    400, "Fayl formati pdf, docx, xls yoki xlsx bo`lishi kerak!")

            image_contents = await agreementFile.read()

            agreementFile.filename = f"{uuid.uuid4()}__{agreementFile.filename}"

            if len(image_contents) > 3000000:
                raise HTTPException(
                    400, "Fayl kattaligi maksimal 3 MB!")

            new_clientAgreement = ClientAgreement(
                fileName=agreementFile.filename,
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

                old_file_path = f"assets/clientAgreements/{this_clientAgreement.agreementFile}"

                if agreementFile:

                    if not agreementFile.content_type in CONTENT_TYPE_LOOKUP_TABLE:
                        raise HTTPException(
                            400, "Fayl formati pdf, docx, xls yoki xlsx bo`lishi kerak!")

                    file_contents = await agreementFile.read()

                    filename = f"{uuid.uuid4()}__{agreementFile.filename}"
                    if len(file_contents) > 3000000:
                        raise HTTPException(
                            400, "Fayl kattaligi maksimal 3 MB!")
                else:
                    filename = this_clientAgreement.agreementFile
                    file_contents = None

                clientAgreement.update({
                    ClientAgreement.fileName: filename,
                    ClientAgreement.shopId: shopId,
                    ClientAgreement.clientId: clientId,
                    ClientAgreement.monthlyFee: monthlyFee,
                    ClientAgreement.balance: balance,
                    ClientAgreement.status: status,
                    ClientAgreement.type: type,
                    ClientAgreement.startedAt: startedAt,
                    ClientAgreement.liablePerson: liablePerson,
                })
                db.commit()

                if file_contents:
                    with open(f"assets/clientAgreementAgreements/{filename}", "wb") as f:
                        f.write(file_contents)

                        if exists(old_file_path):
                            os.unlink(old_file_path)

                raise HTTPException(
                    status_code=200, detail="O`zgarish saqlandi!")
            else:
                raise HTTPException(
                    status_code=400, detail="So`rovda xatolik!")
        except IntegrityError as e:
            integrityHandler(e)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")