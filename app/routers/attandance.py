from datetime import datetime
import json
from fastapi import HTTPException, APIRouter, Depends, Request
from typing import Optional
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
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_all_attandances(search, page, limit, usr, db)  
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")  

@attandance_router.post("/attandance/create", description="This router is able to add new attandance")
async def create_new_attandance(
    form_data: NewAttandance,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_attandance(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@attandance_router.put("/attandance/{id}/update", description="This router is able to update attandance")
async def update_one_attandance(
    id: int,
    form_data: UpdateAttandance,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_attandance(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@attandance_router.post("/attandance/face-id", include_in_schema=False)
async def get_attandance_users_list(
    req: Request,
    db:Session = ActiveSession,
):   
    
    try:
        data  = await req.body()
        data_str = data.decode()
        data_str = data_str.split("\n",3)[3]
        data_str = data_str[:-20]

        # with open(f"{uuid.uuid4()}.json", "w") as f:
        #     f.write(data_str)
        
        data_dict = json.loads(data_str)
        AccessControllerEvent = data_dict['AccessControllerEvent']
        user_id = AccessControllerEvent['employeeNoString']
        attendanceStatus = AccessControllerEvent['attendanceStatus']
        deviceName = AccessControllerEvent['deviceName']

       

        date_str = data_dict['dateTime']
        date_obj = datetime.fromisoformat(date_str[:-6])  # remove timezone offset
        formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")

        if attendanceStatus == 'checkIn':
            type = 'entry'
        else:
            type = 'exit'

        if attendanceStatus:

            await makeDavomat(user_id, type, formatted_date, deviceName, db)

            return "success"
    except Exception as e:
        print(e.args)