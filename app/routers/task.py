from datetime import date
from fastapi import Body, File, HTTPException, APIRouter, Depends, UploadFile
from typing import Optional, List
from app.schemas.user import NewUser
from app.utils.fileUtil import save_file, validate_file
from app.utils.handler import integrityHandler
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import Session
from app.models.task import *
from app.functions.task import *
from app.schemas.task import *
from app.utils.wsmanager import manager

task_router = APIRouter(tags=['Xabar Endpoint'])

@task_router.get("/task/roles")
async def get_tasks_list(
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_tasks_roles(usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@task_router.get("/notifications")
async def get_notifications_list(
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_notifications(usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@task_router.get("/tasks")
async def get_tasks_list(
    search: Optional[str] = "",
    forRole: ChatTypes = 'headCleaner',
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_tasks(search, forRole, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
    
@task_router.put("/task/see")
async def see_task(
    id: int,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return make_view_task(id, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@task_router.get("/task/one")
async def get_task(
    id: int,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return db.get(Task, id)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
    
@task_router.put("/notification/see")
async def see_notification(
    id: int,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return make_view_notification(id, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@task_router.post("/task/create")
async def create_new_task(
    fileName: Optional[UploadFile] = File(...),
    context: Optional[str] = Body(...),
    forRole: ChatTypes = Body(...),
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if  usr.userRole in ['director', 'accountant', 'clerk']:
        try:

            _fileName = await validate_file(fileName, ['document', 'image', 'audio', 'video'], 3)

            new_task = Task(
                fileName=_fileName,
                context=context,
                employeeId=usr.employeeId,
                forRole=forRole,
                branchId=usr.branchId,
            )

            db.add(new_task)
            db.commit()
            db.refresh(new_task)

            dateTime = date.today().strftime("%Y/%m/%d")

            await save_file(fileName, _fileName, f"{new_task.forRole}/{dateTime}")
            await manager.send_user(new_task.context, [new_task.forRole], 'task', new_task.id, usr, db)

            raise HTTPException(200, "Ma`lumotlar saqlandi!")
        except IntegrityError as e:
            raise integrityHandler(e)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
    
@task_router.post("/task/{id}/complete")
async def complete_task(
    id: int,
    responseFileName: Optional[UploadFile] = File(...),
    responseText: Optional[str] = Body(...),
    responseType: TaskTypes = Body(...),
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if not usr.userRole in ['director', 'accountant', 'clerk']:
        try:

            _task = db.query(Task).filter_by(id=id, forRole=usr.role, responseEmployeeId=None).first()
            if not _task:
                raise HTTPException(400, 'Ushbu vazifa uchun siz javobgar emassiz!')

            _fileName = await validate_file(responseFileName, ['document', 'image', 'audio', 'video'], 3)

            _task.responseFileName = _fileName
            _task.responseType = responseType
            _task.responseText = responseText
            _task.responseEmployeeId = usr.employeeId
            _task.completedAt = func.now()

            db.commit()

            dateTime = date.today().strftime("%Y/%m/%d")

            await save_file(responseFileName, _fileName, f"{_task.forRole}/{dateTime}")
            await manager.send_user(_task.responseText, [_task.employee.role], 'task', _task.id, usr, db)

            raise HTTPException(200, "Ma`lumotlar saqlandi!")
        except IntegrityError as e:
            raise integrityHandler(e)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@task_router.delete("/task/{id}/delete")
async def remove_tasks(
    ids: List[int],
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):

    try:
        db.query(Task).filter(Task.id.in_(ids), Task.userId == usr.id).delete()
        db.commit()
        return HTTPException(200, 'O\'chirildi!')
    except IntegrityError as e:
        integrityHandler(e)


# @task_router.put("/task/{id}/update", description="This router is able to update task")
# async def update_one_task(
#     id: int,
#     form_data: Updatetask,
#     db: Session = ActiveSession,
#     usr: NewUser = Depends(get_current_active_user)
# ):
#     if not usr.userRole in ['any_role']:
#         return update_task(id, form_data, usr, db)
#     else:
#         raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
