from os.path import exists
import os
import uuid
from fastapi import Body, File, Form, HTTPException, APIRouter, Depends, UploadFile
from typing import Optional
from app.schemas.enums import EmployeeRoles
from app.schemas.user import NewUser
from app.utils.handler import integrityHandler
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.employee import *
from app.functions.employee import *

employee_router = APIRouter(tags=['Employee Endpoint'])


CONTENT_TYPE_LOOKUP_TABLE = [
    "application/pdf",
    "application/x-excel",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
]


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


@employee_router.post("/employee/create", description="This router is able to add new employee")
async def create_new_employee(
    firstname: str = Body(..., max_length=20),
    lastname: str = Body(..., max_length=20),
    phoneNumber: int = Body(..., min=100000000, max=999999999),
    passportSeriaNumber: str = Body(..., max_length=10),
    salaryQuantity: float = Body(..., ge=0),
    role: EmployeeRoles = Body(...),
    agreementFile: UploadFile = File(...),
    duty: str = Body(..., max_length=255),
    shiftId: int = Body(...),
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:

        try:

            if not agreementFile.content_type in CONTENT_TYPE_LOOKUP_TABLE:
                raise HTTPException(
                    400, "Fayl formati pdf, docx, xls yoki xlsx bo`lishi kerak!")

            image_contents = await agreementFile.read()

            agreementFile.filename = f"{uuid.uuid4()}__{agreementFile.filename}"

            if len(image_contents) > 3000000:
                raise HTTPException(
                    400, "Fayl kattaligi maksimal 3 MB!")

            new_employee = Employee(
                firstname=firstname,
                lastname=lastname,
                phoneNumber=phoneNumber,
                passportSeriaNumber=passportSeriaNumber,
                salaryQuantity=salaryQuantity,
                role=role,
                agreementFile=agreementFile.filename,
                duty=duty,
                branchId=usr.branchId,
                shiftId=shiftId,
            )

            db.add(new_employee)
            db.commit()

            with open(f"assets/employeeAgreements/{agreementFile.filename}", "wb") as f:
                f.write(image_contents)

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
    passportSeriaNumber: str = Body(..., max_length=10),
    salaryQuantity: float = Body(..., ge=0),
    role: EmployeeRoles = Body(...),
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

                old_file_path = f"assets/employeeAgreements/{this_employee.agreementFile}"

                if agreementFile:

                    if not agreementFile.content_type in CONTENT_TYPE_LOOKUP_TABLE:
                        raise HTTPException(
                            400, "Fayl formati pdf, docx, xls yoki xlsx bo`lishi kerak!")

                    file_contents = await agreementFile.read()

                    filename = f"{uuid.uuid4()}__{agreementFile.filename}"
                    if len(file_contents) > 3000000:
                        raise HTTPException(
                            400, "Fayl kattaligi maksimal 3 MB!")
                else:
                    filename = this_employee.agreementFile
                    file_contents = None

                employee.update({
                    Employee.firstname: firstname,
                    Employee.lastname: lastname,
                    Employee.phoneNumber: phoneNumber,
                    Employee.passportSeriaNumber: passportSeriaNumber,
                    Employee.salaryQuantity: salaryQuantity,
                    Employee.role: role,
                    Employee.agreementFile: filename,
                    Employee.duty: duty,
                    Employee.fired: fired,
                    Employee.shiftId: shiftId,
                })
                db.commit()

                if file_contents:
                    with open(f"assets/employeeAgreements/{filename}", "wb") as f:
                        f.write(file_contents)

                        if exists(old_file_path):
                            os.unlink(old_file_path)

                raise HTTPException(
                    status_code=200, detail="O`zgarish saqlandi!")
            else:
                raise HTTPException(
                    status_code=400, detail="So`rovda xatolik!")
        except IntegrityError as e:
            integrityHandler(e)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")