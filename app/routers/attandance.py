from datetime import datetime, date
import json
import re
from fastapi import HTTPException, APIRouter, Depends, Request
from typing import Optional, List
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
    aDate: date,
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_attended_employees(search, aDate, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@attandance_router.get("/attandances/employee", description="This router returns list of the attandances using pagination")
async def get_attandances_list(
    id: int,
    fromDate: date,
    toDate: date,
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_attandances(id, fromDate, toDate, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@attandance_router.post("/attandance/create", description="This router is able to add new attandance")
async def create_new_attandance(
    form_datas: List[NewAttandance],
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        for form_data in form_datas:
            await makeDavomat(form_data.employeeId, form_data.type, form_data.created_at, usr.employee.fullname(), db)
        return 'success'
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@attandance_router.put("/attandance/{id}/update", description="This router is able to update attandance")
async def update_one_attandance(
    id: int,
    form_data: UpdateAttandance,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_attandance(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@attandance_router.post("/attandance/face-id", include_in_schema=False)
async def get_attandance_users_list(
    req: Request,
    db: Session = ActiveSession,
):

    try:
        data = await req.body()
        data_str = data.decode()
        match = re.search(r'\{.*\}', data_str, re.DOTALL)
        json_data = match.group(0) if match else None

        # Load JSON data into a Python dictionary
        data_dict = json.loads(json_data) if json_data else None

        AccessControllerEvent = data_dict['AccessControllerEvent']
        user_id = AccessControllerEvent['employeeNoString']
        attendanceStatus = AccessControllerEvent['attendanceStatus']
        deviceName = AccessControllerEvent['deviceName']

        date_str = data_dict['dateTime']
        date_obj = datetime.fromisoformat(
            date_str[:-6])  # remove timezone offset
        formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")

        if attendanceStatus:

            await makeDavomat(user_id, attendanceStatus, formatted_date, deviceName, db)

            return "success"
    except Exception as e:
        print(e.args)
