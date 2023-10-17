import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.employee import *
from app.schemas.employee import *

def get_all_employees(search, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit
    
    employees = db.query(Employee)

    #if search:
       #employees = employees.filter(
           #Employee.id.like(f"%{search}%"),
       #)

    
    all_data = employees.order_by(Employee.id.desc()).offset(offset).limit(limit)
    count_data = employees.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }

def create_employee(form_data: NewEmployee, usr, db: Session):
    
    try:
        new_employee = Employee(
            firstname=form_data.firstname,
        lastname=form_data.lastname,
        phoneNumber=form_data.phonenumber,
        passportSeriaNumber=form_data.passportserianumber,
        salaryQuantity=form_data.salaryquantity,
        role=form_data.role,
        agreementFile=form_data.agreementfile,
        duty=form_data.duty,
        fired=form_data.fired,
        branchId=form_data.branchid,
        shiftId=form_data.shiftid,
    )

        db.add(new_employee)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)

def update_employee(id, form_data: UpdateEmployee, usr, db: Session):
    
    try:
        employee = db.query(Employee).filter(Employee.id == id)
        this_employee = employee.first()
        if this_employee:
            employee.update({    
            Employee.firstname: form_data.firstname,
            Employee.lastname: form_data.lastname,
            Employee.phoneNumber: form_data.phonenumber,
            Employee.passportSeriaNumber: form_data.passportserianumber,
            Employee.salaryQuantity: form_data.salaryquantity,
            Employee.role: form_data.role,
            Employee.agreementFile: form_data.agreementfile,
            Employee.duty: form_data.duty,
            Employee.fired: form_data.fired,
            Employee.branchId: form_data.branchid,
            Employee.shiftId: form_data.shiftid,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
    
