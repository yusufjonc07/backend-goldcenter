import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import label
from fastapi import HTTPException
from app.models.attandance import *
from app.models.salary import *
from app.schemas.attandance import *
from app.utils.pagination import pagination
from datetime import date, datetime


def get_all_attandances(search, page, limit, usr, db: Session):


    attandances = db.query(Attandance)

    # if search:
    # attandances = attandances.filter(
    # Attandance.id.like(f"%{search}%"),
    # )

    return pagination(attandances, page, limit)




def get_attended_employees(search, page, limit, usr, db: Session):

    attandanded_employees = db.query(
        label('employeeId', Employee.id),
        label('employeeName', Employee._fullname),
        label('workBeginTime', Shift.workBeginTime),
        label('workEndTime', Shift.workEndTime),
        label('date', func.date(Attandance.created_at)),
    ).select_from(Employee).join(Employee.shift).join(Employee.attandances)\
    .group_by(func.date(Attandance.created_at))

    # if search:
    #   attandances = attandances.filter(
    #   Attandance.id.like(f"%{search}%"),
    # )

    return pagination(attandanded_employees, page, limit)


def update_attandance(id, form_data: UpdateAttandance, usr, db: Session):

    try:
        attandance = db.query(Attandance).filter(Attandance.id == id)
        this_attandance = attandance.first()
        if this_attandance:
            attandance.update({
                Attandance.type: form_data.type,
                Attandance.employeeId: form_data.employeeid,
                Attandance.workTime: form_data.worktime,
                Attandance.authorizator: form_data.authorizator,
                Attandance.created_at: form_data.created_at,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)


async def makeDavomat(employeeId, type, dateTime, authorizatorName, db: Session):

    employee = db.query(Employee).filter_by(id=employeeId).first()
    if not employee:
        raise HTTPException(status_code=400, detail="Hodim topilmadi!")

    last_davomat = db.query(Attandance).filter(
        Attandance.employeeId == employee.id).order_by(Attandance.created_at.desc()).first()

    error = workTime = 0

    dav_type = 'entry'
    if type == 'any':
        if last_davomat:
            if last_davomat.type == 'entry':
                dav_type = 'exit'

    elif type == 'entry':

        if last_davomat and last_davomat.type == 'entry':
            error += 1

    elif type == 'exit':

        if last_davomat:

            if last_davomat.type != 'entry':
                error += 1
            else:
                dav_type = 'exit'

        else:
            error += 1

    if error == 0:

        yearMonth = datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S")

        print(dateTime)

        attandance_count = db.query(Attandance).filter(
            func.year(Attandance.created_at) == yearMonth.year,
            func.month(Attandance.created_at) == yearMonth.month,
            Attandance.employeeId == employee.id,
            Attandance.type == 'entry',
        ).count()

        if attandance_count == 0:
            new_salary = Salary(
                employeeId=employee.id,
                calcWage=employee.salaryQuantity,
                createdAt=dateTime,
            )

            db.add(new_salary)
        

        new_attandance = Attandance(
            type=dav_type,
            employeeId=employee.id,
            workTime=workTime,
            authorizator=authorizatorName,
            created_at=dateTime,
        )

        db.add(new_attandance)
        db.commit()
