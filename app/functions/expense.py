import math
from sqlalchemy.orm import aliased, Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.expense import *
from app.models.contragent import Contragent
from app.schemas.expense import *
from sqlalchemy.sql import label
from app.utils.handler import integrityHandler
from app.utils.pagination import pagination
from typing import List


def get_all_expenses(moneyFormId, search, type, fromDate, toDate, employeeId, contragentId, page, limit, usr, db: Session):

    worker_alias = aliased(Employee, name='worker_alias')

    worker = db.query(func.concat(worker_alias.firstname, ' ', worker_alias.lastname)).filter_by(
        id=Expense.employeeId).scalar_subquery()
    regularExpence = db.query(Contragent.name).filter_by(
        id=Expense.contragentId).scalar_subquery()

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

    if contragentId > 0:
        expenses = expenses.filter(
            Expense.contragentId == contragentId)

    if fromDate and toDate:
        expenses = expenses.filter(
            func.date(Expense.createdAt) >= fromDate,
            func.date(Expense.createdAt) <= toDate,
        )

    # if search:
        # expenses = expenses.filter(
        # Expense.id.like(f"%{search}%"),
    # )

    expenses = expenses.order_by(Expense.createdAt.desc())

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


def validate_employees_by_pnfl(employee_pnfls, db: Session):

    unique_employee_pnfls = list(set(employee_pnfls))
    not_found_pnfls = []

    # validate
    for pnfl in unique_employee_pnfls:
        employee = db.query(Employee).filter_by(pnfl=pnfl).first()
        if not employee:
            not_found_pnfls.append(pnfl)

    if len(not_found_pnfls) > 0:
        raise HTTPException(400, ", ".join(not_found_pnfls) +
                            ". Bu PNFL lardagi hodimlar topilmadi!")

    return True


def validate_money_forms_by_name(money_form_names, db: Session):

    unique_money_form_names = list(set(money_form_names))
    not_found_names = []

    for name in unique_money_form_names:
        money_form = db.query(Moneyform).filter_by(name=name).first()
        if not money_form:
            not_found_names.append(name)

    if len(not_found_names) > 0:
        raise HTTPException(400, ", ".join(not_found_names) +
                            ". Bu nomlardagi kassalar topilmadi!")

    return True


def validate_excel_ws(worksheet, db: Session):

    # pnfl array
    employee_pnfls = []

    # money form array
    money_form_names = []

    # get first 1000 rows from worksheet
    for row in worksheet.iter_rows(min_row=2, max_col=7, max_row=1000):

        # stop a loop when the cell is empty
        if row[0].value is None:
            break

        employee_pnfls.append(str(row[0].value))
        money_form_names.append(str(row[2].value))

    validate_employees_by_pnfl(employee_pnfls, db)
    validate_money_forms_by_name(money_form_names, db)


def create_expense_by_ecxel_data(excel_datas: List[NewExpenseExcel], db: Session, usr: User):

    for excel_data in excel_datas:

        employee = db.query(Employee).filter_by(pnfl=excel_data.pnfl).first()
        moneyForm = db.query(Moneyform).filter_by(
            name=excel_data.moneyFormName).first()

        employee.balance -= excel_data.value

        try:
            new_expense = Expense(
                type="salary",
                employeeId=employee.id,
                value=excel_data.value,
                moneyFormId=moneyForm.id,
                branchId=usr.branchId,
                comment="-",
                userId=usr.id,
                isAvanse=excel_data.isAvanse,
                fileName=None,
                createdAt=excel_data.date,
            )

            db.add(new_expense)
            db.flush()

            if new_expense.moneyForm.balance < new_expense.value:
                raise HTTPException(
                    400, f"{new_expense.moneyForm.name} balansida yetarli mablag' yetarli emas!")
            else:
                new_expense.moneyForm.balance -= new_expense.value

        except IntegrityError as e:
            raise integrityHandler(e)

    db.commit()
    raise HTTPException(status_code=200, detail="Ma'lumotlar saqlandi!")
