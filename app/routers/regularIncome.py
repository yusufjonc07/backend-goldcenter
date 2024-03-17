from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.regularIncome import *
from app.functions.regularIncome import *
from app.schemas.regularIncome import *

regularIncome_router = APIRouter(tags=['Doimiy Kirim Endpoint'])


@regularIncome_router.get("/regularIncomes", description="This router returns list of the regularIncomes using pagination")
async def get_regularIncomes_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_regularIncomes(search, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@regularIncome_router.post("/regularIncome/create", description="This router is able to add new regularIncome")
async def create_new_regularIncome(
    form_data: NewRegularincome,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_regularIncome(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@regularIncome_router.put("/regularIncome/{id}/update", description="This router is able to update regularIncome")
async def update_one_regularIncome(
    id: int,
    form_data: UpdateRegularincome,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_regularIncome(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
