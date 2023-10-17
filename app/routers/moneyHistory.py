from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.moneyHistory import *
from app.functions.moneyHistory import *
from app.schemas.moneyHistory import *

moneyHistory_router = APIRouter(tags=['Moneyhistory Endpoint'])

@moneyHistory_router.get("/moneyHistorys", description="This router returns list of the moneyHistorys using pagination")
async def get_moneyHistorys_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_all_moneyHistorys(search, page, limit, usr, db)  
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")  

@moneyHistory_router.post("/moneyHistory/create", description="This router is able to add new moneyHistory")
async def create_new_moneyHistory(
    form_data: NewMoneyhistory,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_moneyHistory(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@moneyHistory_router.put("/moneyHistory/{id}/update", description="This router is able to update moneyHistory")
async def update_one_moneyHistory(
    id: int,
    form_data: UpdateMoneyhistory,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_moneyHistory(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
