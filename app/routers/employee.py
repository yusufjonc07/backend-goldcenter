from datetime import date
from os.path import exists
import os
import uuid
from fastapi import Body, File, Form, HTTPException, APIRouter, Depends, UploadFile
from typing import Optional
from app.schemas.enums import EmployeeRoles
from app.schemas.user import NewUser
from app.utils.fileUtil import replace_file, save_file, validate_file
from app.utils.handler import integrityHandler
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session, load_only
from app.models.employee import *
from app.functions.employee import *

employee_router = APIRouter(tags=['Hodimalar Endpoint'])

@employee_router.get("/employees", description="This router returns list of the employees using pagination")
async def get_employees_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_employees(search, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@employee_router.get("/employee/{id}/details")
async def get_employee_details(
    id: int,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    
    '''
    Hodimning avatarini olish: `/files/employeeAvatars/`\n
    Hodimning passportini olish: `/files/employeePassports/`\n
    Hodimning agreementini olish: `/files/employeeAgreements/`
    '''

    if not usr.userRole in ['any_role']:
        return db.query(Employee)\
            .options(joinedload(Employee.user).options(
                load_only('username')
            ))\
            .filter_by(id=id).first()
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@employee_router.post("/employee/create", description="This router is able to add new employee")
async def create_new_employee(
    firstname: str = Body(..., max_length=20),
    lastname: str = Body(..., max_length=20),
    phoneNumber: int = Body(..., min=100000000, max=999999999),
    agreementFile: UploadFile = File(...),
    passportFile: UploadFile = File(...),
    avatarFile: Optional[UploadFile] = File(None),
    salaryQuantity: float = Body(..., ge=0),
    birthDate: date = Body(...),
    role: EmployeeRoles = Body(...),
    duty: str = Body(..., max_length=255),
    shiftId: int = Body(...),
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        try:

            agreementFileName = await validate_file(agreementFile, ['document', 'image'], 3)
            passportFileName = await validate_file(passportFile, ['image'], 3)

            if avatarFile:
                avatarFileName = await validate_file(avatarFile, ['image'], 3)
            else:
                avatarFileName = None

            if avatarFileName:
                await save_file(avatarFile, avatarFileName, 'employeeAvatars')
           
            await save_file(agreementFile, agreementFileName, 'employeeAgreements')
            await save_file(passportFile, passportFileName, 'employeePassports')


            new_employee = Employee(
                firstname=firstname,
                lastname=lastname,
                phoneNumber=phoneNumber,
                birthDate=birthDate,
                avatarFile=avatarFileName,
                passportFile=passportFileName,
                salaryQuantity=salaryQuantity,
                role=role,
                agreementFile=agreementFileName,
                duty=duty,
                branchId=usr.branchId,
                shiftId=shiftId,
            )

            db.add(new_employee)
            db.commit()

           
            raise HTTPException(200, "Ma`lumotlar saqlandi!")
        except IntegrityError as e:
            raise HTTPException(400, e.args)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@employee_router.put("/employee/{id}/update", description="This router is able to update employee")
async def update_one_employee(
    id: int,
    firstname: str = Body(..., max_length=20),
    lastname: str = Body(..., max_length=20),
    phoneNumber: int = Body(..., min=100000000, max=999999999),
    passportFile: UploadFile = File(None),
    avatarFile: Optional[UploadFile] = File(None),
    salaryQuantity: float = Body(..., ge=0),
    role: EmployeeRoles = Body(...),
    birthDate: date = Body(...),
    agreementFile: Optional[UploadFile] = File(None),
    fired: Optional[bool] = Body(False),
    duty: str = Body(..., max_length=255),
    shiftId: int = Body(...),
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        try:
            employee = db.query(Employee).filter(Employee.id == id)
            this_employee = employee.first()
            if this_employee:   

                _old_employee = this_employee

                if avatarFile:
                    avatarFileName = await validate_file(avatarFile, ['image'], 3)
                else:
                    avatarFileName = this_employee.avatarFile

                if passportFile:
                    passportFileName = await validate_file(passportFile, ['image'], 3)
                else:
                    passportFileName = this_employee.passportFile

                if agreementFile:
                    agreementFileName = await validate_file(agreementFile, ['document'], 3)
                else:
                    agreementFileName = this_employee.agreementFile

                employee.update({
                    Employee.firstname: firstname,
                    Employee.lastname: lastname,
                    Employee.phoneNumber: phoneNumber,
                    Employee.salaryQuantity: salaryQuantity,
                    Employee.role: role,
                    Employee.agreementFile: agreementFileName,
                    Employee.birthDate: birthDate,
                    Employee.avatarFile: avatarFileName,
                    Employee.passportFile: passportFileName,
                    Employee.duty: duty,
                    Employee.fired: fired,
                    Employee.shiftId: shiftId,
                })
                db.commit()

                await replace_file(passportFile, _old_employee.passportFile, passportFileName, 'employeePassports')
                await replace_file(agreementFile, _old_employee.agreementFile, agreementFileName, 'employeeAgreements')
                await replace_file(avatarFile, _old_employee.avatarFile, avatarFileName, 'employeeAvatars')

                raise HTTPException(
                    status_code=200, detail="O`zgarish saqlandi!")
            else:
                raise HTTPException(
                    status_code=400, detail="So`rovda xatolik!")
        except IntegrityError as e:
            integrityHandler(e)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")