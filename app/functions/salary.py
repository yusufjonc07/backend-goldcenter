from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.salary import *
from app.models.expense import *
from app.models.attandance import *
from app.schemas.salary import *
from app.utils.handler import integrityHandler
from app.utils.pagination import pagination
from sqlalchemy.sql import label, distinct


def get_all_salarys(search, year, month,   usr, db: Session, employeeId=0):

    # how many days employee attandanded in a month
    attandance_count = db.query(func.count(distinct(func.date(Attandance.created_at)))).filter(
        func.year(Attandance.created_at) == year,
        func.month(Attandance.created_at) == month,
        Attandance.employeeId == Salary.employeeId,
        Attandance.type == 'checkIn',
    ).group_by(Attandance.employeeId).subquery()

    # how many salary advance employee received in a month
    advance_sum = db.query(func.sum(Expense.value)).filter(
        func.year(Expense.createdAt) == year,
        func.month(Expense.createdAt) == month,
        Expense.employeeId == Salary.employeeId,
        Expense.type == 'salary',
    ).subquery()

    salarys = db.query(
        label("employeeId", Employee.id),
        label("salaryId", Salary.id),
        label("employeeName", func.concat(
            Employee.firstname, ' ', Employee.lastname)),
        label("attandanceCount", attandance_count),
        label("calcWage", Salary.calcWage),
        label("isConfirmed", Salary.isConfirmed),
        label("salaryAdvance", func.coalesce(advance_sum, 0)),
    ).join(Salary.employee).filter(
        func.year(Salary.createdAt) == year,
        func.month(Salary.createdAt) == month,
    )

    if employeeId > 0:
        salarys = salarys.filter(Salary.employeeId == employeeId)

    if search:
        salarys = salarys.filter(
            Employee.firstname.like(f"%{search}%"),
            Employee.lastname.like(f"%{search}%"),
            Employee.phoneNumber.like(f"%{search}%"),
        )

    return salarys.all()


def pay_all_salarys(salariesId: list, usr, db):
    for salaryId in salariesId:

        salary: Salary = db.get(Salary, salaryId)
        # how many salary advance employee received in a month
        advance_sum = db.query(func.sum(Expense.value)).filter(
            func.year(Expense.createdAt) == func.year(salary.createdAt),
            func.month(Expense.createdAt) == func.month(salary.createdAt),
            Expense.employeeId == salary.employeeId,
            Expense.type == 'salary',
        ).scalar()

        if not advance_sum:
            advance_sum = 0

        if not salary or salary.isConfirmed == True:
            raise HTTPException(400, "Bu oy uchun yozilgan maosh topilmadi")
        elif salary.calcWage > advance_sum:
            raise HTTPException(400, "Oylik maosh to'liq to'lanmadi")
        else:

            employee = salary.employee
            employee.balance += salary.calcWage
            salary.isConfirmed = True

    db.commit()


def update_salary(id, form_data: UpdateSalary, usr, db: Session):

    try:
        salary = db.query(Salary).filter(
            Salary.id == id, Salary.isConfirmed == False)
        this_salary = salary.first()
        if this_salary:
            salary.update({
                Salary.calcWage: form_data.calcwage,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise integrityHandler(e)
