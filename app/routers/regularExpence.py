from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.regularExpence import *
from app.functions.regularExpence import *
from app.schemas.regularExpence import *

regularExpence_router = APIRouter(tags=['Doimiy Chiqim Endpoint'])


@regularExpence_router.get("/regularExpences", description="This router returns list of the regularExpences using pagination")
async def get_regularExpences_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_regularExpences(search, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@regularExpence_router.post("/regularExpence/create", description="This router is able to add new regularExpence")
async def create_new_regularExpence(
    form_data: NewRegularexpence,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_regularExpence(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@regularExpence_router.put("/regularExpence/{id}/update", description="This router is able to update regularExpence")
async def update_one_regularExpence(
    id: int,
    form_data: UpdateRegularexpence,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_regularExpence(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
