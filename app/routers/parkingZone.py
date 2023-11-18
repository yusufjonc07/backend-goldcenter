from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.parkingZone import *
from app.functions.parkingZone import *
from app.schemas.parkingZone import *

parkingZone_router = APIRouter(tags=['Parkovka Endpoint'])


@parkingZone_router.get("/parkingZones", description="This router returns list of the parking zones using pagination")
async def get_parkingZones_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_parkingZones(search, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@parkingZone_router.post("/parkingZone/create", description="This router is able to add new parkingZone")
async def create_new_parkingZone(
    form_data: NewParkingZone,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_parkingZone(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@parkingZone_router.put("/parkingZone/{id}/update", description="This router is able to update parkingZone")
async def update_one_parkingZone(
    id: int,
    form_data: UpdateParkingZone,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_parkingZone(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
