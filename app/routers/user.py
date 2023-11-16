from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.user import *
from app.functions.user import *
from app.schemas.user import *

user_router = APIRouter(tags=['Foydalanuvchilar Endpoint'])

@user_router.get("/users", description="This router returns list of the users using pagination")
async def get_users_list(
    search: Optional[str] = "",
    employeeId: Optional[int] = 0,
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_all_users(search, employeeId, page, limit, usr, db)  
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")  

@user_router.post("/user/create", description="This router is able to add new user")
async def create_new_user(
    form_data: NewUser,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_user(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@user_router.put("/user/{id}/update", description="This router is able to update user")
async def update_one_user(
    id: int,
    form_data: UpdateUser,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_user(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
