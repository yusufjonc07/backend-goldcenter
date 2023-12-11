from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.salary import *
from app.functions.salary import *
from app.schemas.salary import *

salary_router = APIRouter(tags=['Salary Endpoint'])

@salary_router.get("/salaries", description="This router returns list of the salarys using pagination")
async def get_salarys_list(
    year: int,
    month: int,
    search: Optional[str] = "",
    employeeId: Optional[int] = 0,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_all_salarys(search, year, month, usr, db, employeeId)  
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")  


@salary_router.put("/salary/{id}/update", description="This router is able to update salary")
async def update_one_salary(
    id: int,
    form_data: UpdateSalary,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_salary(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
