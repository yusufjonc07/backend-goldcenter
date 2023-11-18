from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.parkingCar import *
from app.functions.parkingCar import *
from app.schemas.parkingCar import *

parkingCar_router = APIRouter(tags=['ParkingCar Endpoint'])

@parkingCar_router.get("/parkingCars", description="This router returns list of the parkingCars using pagination")
async def get_parkingCars_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_all_parkingCars(search, page, limit, usr, db)  
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")  

@parkingCar_router.post("/parkingCar/enter", description="This router is able to add new parkingCar")
async def create_new_parkingCar(
    form_data: NewParkingCar,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return enter_parkingCar(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@parkingCar_router.put("/parkingCar/exit")
async def exit_one_parkingCar(
    form_data: UpdateParkingCar,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return exit_parkingCar(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
