from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.moneyForm import *
from app.functions.moneyForm import *
from app.schemas.moneyForm import *

moneyForm_router = APIRouter(tags=['To`lov turi Endpoint'])

@moneyForm_router.get("/moneyForms", description="This router returns list of the moneyForms using pagination")
async def get_moneyForms_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_all_moneyForms(search, page, limit, usr, db)  
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")  

@moneyForm_router.post("/moneyForm/create", description="This router is able to add new moneyForm")
async def create_new_moneyForm(
    form_data: NewMoneyform,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_moneyForm(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@moneyForm_router.put("/moneyForm/{id}/update", description="This router is able to update moneyForm")
async def update_one_moneyForm(
    id: int,
    form_data: UpdateMoneyform,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_moneyForm(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
