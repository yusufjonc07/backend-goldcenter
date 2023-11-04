from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.attandance import *
from app.functions.attandance import *
from app.schemas.attandance import *

attandance_router = APIRouter(tags=['Davomat Endpoint'])

@attandance_router.get("/attandances", description="This router returns list of the attandances using pagination")
async def get_attandances_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_all_attandances(search, page, limit, usr, db)  
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")  

@attandance_router.post("/attandance/create", description="This router is able to add new attandance")
async def create_new_attandance(
    form_data: NewAttandance,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_attandance(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@attandance_router.put("/attandance/{id}/update", description="This router is able to update attandance")
async def update_one_attandance(
    id: int,
    form_data: UpdateAttandance,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_attandance(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
