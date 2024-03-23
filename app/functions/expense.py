import math
from sqlalchemy.orm import aliased, Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.expense import *
from app.models.regularExpence import RegularExpence
from app.schemas.expense import *
from sqlalchemy.sql import label
from app.utils.handler import integrityHandler
from app.utils.pagination import pagination


def get_all_expenses(moneyFormId, search, type, fromDate, toDate, employeeId, regularExpenceId, page, limit, usr, db: Session):

    worker_alias = aliased(Employee, name='worker_alias')

    worker = db.query(func.concat(worker_alias.firstname, ' ', worker_alias.lastname)).filter_by(
        id=Expense.employeeId).scalar_subquery()
    regularExpence = db.query(RegularExpence.name).filter_by(
        id=Expense.regularExpenceId).scalar_subquery()

    expenses = db.query(
        label('type', Expense.type),
        label('worker', worker),
        label('regularExpence', regularExpence),
        label('comment', Expense.comment),
        label('user', func.concat(Employee.firstname, ' ', Employee.lastname)),
        label('createdAt', Expense.createdAt),
        label('value', Expense.value),
        label('isAvanse', Expense.isAvanse),
        label('moneyForm', Moneyform.name),
    ).join(Expense.user).join(User.employee).join(Expense.moneyForm)

    if type:
        expenses = expenses.filter(Expense.type == type)

    if employeeId > 0:
        expenses = expenses.filter(Expense.employeeId == employeeId)

    if moneyFormId > 0:
        expenses = expenses.filter(Expense.moneyFormId == moneyFormId)

    if regularExpenceId > 0:
        expenses = expenses.filter(
            Expense.regularExpenceId == regularExpenceId)

    if fromDate and toDate:
        expenses = expenses.filter(
            func.date(Expense.createdAt) >= fromDate,
            func.date(Expense.createdAt) <= toDate,
        )

    # if search:
        # expenses = expenses.filter(
        # Expense.id.like(f"%{search}%"),
    # )

    return pagination(expenses, page, limit)


def create_expense(form_data: NewExpense, usr, db: Session):

    try:
        new_expense = Expense(
            type=form_data.type,
            employeeId=form_data.employeeid,
            value=form_data.value,
            moneyFormId=form_data.moneyformid,
            comment=form_data.comment,
            userId=form_data.userid,
            fileName=form_data.filename,
            createdAt=form_data.createdat,
            branchId=form_data.branchid,
            floorId=form_data.floorid,
        )

        db.add(new_expense)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")

    except IntegrityError as e:
        raise integrityHandler(e)


def update_expense(id, form_data: UpdateExpense, usr, db: Session):

    try:
        expense = db.query(Expense).filter(Expense.id == id)
        this_expense = expense.first()
        if this_expense:
            expense.update({
                Expense.type: form_data.type,
                Expense.employeeId: form_data.employeeid,
                Expense.value: form_data.value,
                Expense.moneyFormId: form_data.moneyformid,
                Expense.comment: form_data.comment,
                Expense.userId: form_data.userid,
                Expense.fileName: form_data.filename,
                Expense.createdAt: form_data.createdat,
                Expense.branchId: form_data.branchid,
                Expense.isAvanse: form_data.isAvanse,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
