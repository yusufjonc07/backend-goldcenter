from datetime import date
from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.schemas.enums import ReportTypes
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.shift import *
from app.functions.report import *

report_router = APIRouter(tags=['Hisobotlar Endpoint'])

@report_router.get("/income", description="This router returns list of the reports using pagination")
async def get_reports_list(
    floor_id: Optional[int] = 0,
    year: int = ...,
    month: int = ...,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_income(floor_id, year, month, db)  
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")  
    
@report_router.get("/report/index")
async def get_reports_list(
    fromDate: Optional[date] = date.today(),
    toDate: Optional[date] = date.today(),
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_report_index(fromDate, toDate, db, usr) 
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!") 
    
@report_router.get("/report/income/floor")
async def get_reports_income_floor_list(
    fromDate: Optional[date] = date.today(),
    toDate: Optional[date] = date.today(),
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_report_index_income_floor(fromDate, toDate, db, usr) 
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!") 