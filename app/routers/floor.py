from fastapi import HTTPException, APIRouter, Depends
from typing import List, Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.floor import *
from app.functions.floor import *
from app.schemas.floor import *

floor_router = APIRouter(tags=['Qavat Endpoint'])

@floor_router.get("/floors", description="This router returns list of the floors using pagination")
async def get_floors_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_all_floors(search, page, limit, usr, db)  
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")  

@floor_router.post("/floor/create", description="This router is able to add new floor")
async def create_new_floor(
    form_data: NewFloor,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_floor(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@floor_router.put("/floor/{id}/update", description="This router is able to update floor")
async def update_one_floor(
    id: int,
    form_data: UpdateFloor,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_floor(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
