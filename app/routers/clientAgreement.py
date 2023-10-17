from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.clientAgreement import *
from app.functions.clientAgreement import *
from app.schemas.clientAgreement import *

clientAgreement_router = APIRouter(tags=['Clientagreement Endpoint'])

@clientAgreement_router.get("/clientAgreements", description="This router returns list of the clientAgreements using pagination")
async def get_clientAgreements_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_all_clientAgreements(search, page, limit, usr, db)  
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")  

@clientAgreement_router.post("/clientAgreement/create", description="This router is able to add new clientAgreement")
async def create_new_clientAgreement(
    form_data: NewClientagreement,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_clientAgreement(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@clientAgreement_router.put("/clientAgreement/{id}/update", description="This router is able to update clientAgreement")
async def update_one_clientAgreement(
    id: int,
    form_data: UpdateClientagreement,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_clientAgreement(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
