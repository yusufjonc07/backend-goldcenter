import calendar
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import label, or_
from fastapi import HTTPException
from app.models.attandance import *
from app.models.salary import *
from app.schemas.attandance import *
from app.utils.pagination import pagination
from datetime import date, datetime
from app.utils.handler import integrityHandler


def get_all_attandances(id, fromDate, toDate, page, limit, usr, db: Session):

    attandances = db.query(Attandance).filter(
        Attandance.employeeId == id,
        func.date(Attandance.created_at) >= fromDate,
        func.date(Attandance.created_at) <= toDate,
    ).order_by(Attandance.created_at.desc())

    # if search:
    # attandances = attandances.filter(
    # Attandance.id.like(f"%{search}%"),
    # )

    return pagination(attandances, page, limit)


def get_attended_employees(search, aDate, page, limit, usr, db: Session):

    attandanded_employees = db.query(
        label('employeeId', Employee.id),
        label('employeeName', Employee._fullname),
        label('role', Employee.role),
        label('workBeginTime', Shift.workBeginTime),
        label('workEndTime', Shift.workEndTime),
    ).select_from(Employee).join(Employee.shift).join(Employee.attandances)\
        .filter(func.date(Attandance.created_at) == aDate).group_by(Employee.id)

    if search:
        attandanded_employees = attandanded_employees.filter(
            or_(
                Employee.firstname.like(f"%{search}%"),
                Employee.lastname.like(f"%{search}%"),
            )
        )

    result = pagination(attandanded_employees, page, limit)
    new_data = []

    for employee in result['data']:
        new_attandances = dict(employee)
        new_attandances['attandances'] = db.query(Attandance).filter(
            func.date(Attandance.created_at) == aDate,
            Attandance.employeeId == employee.employeeId
        ).order_by(Attandance.created_at.asc()).all()

        new_data.append(new_attandances)

    result['data'] = new_data

    return result


def employee_attandances(id, year, month, db: Session):
    try:

        days_count = calendar.monthrange(year, month)[1]

        attandances = db.query(
            func.count(Attandance.id).label('count'),
            func.day(Attandance.created_at).label('day')
        ).filter(
            func.year(Attandance.created_at) == year,
            func.month(Attandance.created_at) == month,
            Attandance.type == 'checkIn',
            Attandance.employeeId == id
        ).group_by(func.day(Attandance.created_at)).all()

        days = []

        for day in range(1, days_count+1):
            status = False
            for attd in attandances:
                if attd.day == day and attd.count > 0:
                    status = True

            days.append(status)

        return days

    except IntegrityError as e:
        integrityHandler(e)


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

    dav_type = 'checkIn'
    if type == 'any':
        if last_davomat:
            if last_davomat.type == 'checkIn':
                dav_type = 'checkOut'

    elif type == 'checkIn':

        if last_davomat and last_davomat.type == 'checkIn':
            error += 1

    elif type == 'checkOut':

        if last_davomat:

            if last_davomat.type != 'checkIn':
                error += 1
            else:
                dav_type = 'checkOut'

        else:
            error += 1

    if error == 0:

        yearMonth = datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S")

        print(dateTime)

        salary = db.query(Salary).filter(
            func.year(Salary.createdAt) == yearMonth.year,
            func.month(Salary.createdAt) == yearMonth.month,
            Salary.employeeId == employee.id,
        ).first()

        if not salary:
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
