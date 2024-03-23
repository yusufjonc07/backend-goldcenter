from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.debetHistory import *
from app.functions.debetHistory import *
from app.schemas.debetHistory import *

debetHistory_router = APIRouter(tags=['DebetHistory Endpoint'])


@debetHistory_router.get("/debetHistorys", description="This router returns list of the debetHistorys using pagination")
async def get_debetHistorys_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_debetHistorys(search, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@debetHistory_router.post("/debetHistory/create", description="This router is able to add new debetHistory")
async def create_new_debetHistory(
    form_data: NewDebethistory,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_debetHistory(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@debetHistory_router.put("/debetHistory/{id}/update", description="This router is able to update debetHistory")
async def update_one_debetHistory(
    id: int,
    form_data: UpdateDebethistory,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_debetHistory(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
