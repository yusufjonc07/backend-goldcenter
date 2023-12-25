from fastapi import HTTPException, APIRouter, Depends, UploadFile, File
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.income import *
from app.functions.income import *
from app.schemas.income import *
from app.functions.moneyHistory import get_all_agreement_payments
from datetime import date
from app.utils.fileUtil import save_file, validate_file


income_router = APIRouter(tags=['Kassa Endpoint'])


@income_router.get("/incomes")
async def get_agreement_payments(
    clientId: Optional[int] = 0,
    type: str = None,
    fromDate: Optional[date] = None,
    toDate: Optional[date] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_agreement_payments(clientId, type, fromDate, toDate, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@income_router.post("/income/create", description="This router is able to add new income")
async def create_new_income(
    form_data: NewIncome,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_income(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@income_router.put("/income/{id}/update", description="This router is able to update income")
async def update_one_income(
    id: int,
    form_data: UpdateIncome,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_income(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@income_router.put("/income/{id}/fileUpload")
async def update_one_income(
    id: int,
    file: UploadFile = File(...),
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        fileName = await validate_file(file, ['document', 'image'], 3)
        income = db.query(Income).filter_by(id=id).first()
        income.fileName = fileName
        db.commit()
        await save_file(file, fileName, f"expenses")
        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
