from datetime import date
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import label
from app.models.client import Client
from app.models.employee import Employee
from app.models.floor import Floor
from app.models.expense import Expense
from app.models.contragent import Contragent
from app.models.income import Income
from app.models.moneyForm import Moneyform
from app.models.shop import Shop
from app.models.user import User
from app.functions.client import *
from app.functions.employee import *
from app.functions.contragent import *
import calendar

from app.schemas.enums import ReportTypes

MONTHS_COUNT = 12
MONTHS = {
    1: 'Yanvar',
    2: 'Fevral',
    3: 'Mart',
    4: 'Aprel',
    5: 'May',
    6: 'Iyun',
    7: 'Iyul',
    8: 'Avgust',
    9: 'Sentabr',
    10: 'Oktabr',
    11: 'Noyabr',
    12: 'Dekabr',
}


def get_income(floor_id: int, _year: int, _month: int, db: Session):

    yearlyIncome = 0

    if _month == 0:
        incomes = db.query(
            label("value", func.sum(Income.value)),
            label("month", func.month(Income.createdAt)),
        ).filter(
            func.year(Income.createdAt) == _year,
            Income.value > 0
        )

        if floor_id > 0:
            incomes = incomes.join(Income.client).join(
                Client.shop).filter(Shop.floorId == floor_id)

        incomes = incomes.order_by(
            func.month(Income.createdAt).asc()
        ).group_by(
            func.month(Income.createdAt)
        )

        rangeList = range(1, MONTHS_COUNT+1)

    else:

        incomes = db.query(
            label("value", func.sum(Income.value)),
            label("month", func.DAY(Income.createdAt)),
        ).filter(
            func.month(Income.createdAt) == _month,
            func.year(Income.createdAt) == _year,
            Income.value > 0
        )

        if floor_id > 0:
            incomes = incomes.join(Income.client).join(
                Client.shop).filter(Shop.floorId == floor_id)

        incomes = incomes.order_by(
            func.DAY(Income.createdAt).asc()
        ).group_by(
            func.DAY(Income.createdAt)
        ).all()

        rangeList = range(1, calendar.monthrange(_year, _month)[1]+1)

    incomesByMonths = []

    for month in rangeList:
        for income in incomes:
            if month == income.month:

                incomesByMonths.append({
                    'monthName': MONTHS[month] if _month == 0 else str(month),
                    'value': income.value if income.value > 0 else 0.0,
                })

                yearlyIncome += income.value

    return {
        "incomesByMonths": incomesByMonths,
        "yearlyIncome": yearlyIncome if yearlyIncome > 0 else 0.0,
    }


def get_report_index(fromDate: date, toDate: date, db: Session, usr: User):

    incomes = db.query(
        label("method", Moneyform.name),
        label("value", func.sum(Income.value)),
    ).select_from(Income).join(Income.moneyForm)\
        .filter(
        func.date(Income.createdAt) >= fromDate,
        func.date(Income.createdAt) <= toDate,
    ).group_by(Income.moneyFormId).order_by(Moneyform.name.asc())\
        .all()

    expenses = db.query(
        label("method", Moneyform.name),
        label("value", func.sum(Expense.value)),
    ).select_from(Expense).join(Expense.moneyForm)\
        .filter(
        func.date(Expense.createdAt) >= fromDate,
        func.date(Expense.createdAt) <= toDate,
        Expense.branchId == usr.branchId
    ).group_by(Expense.moneyFormId).order_by(Moneyform.name.asc())\
        .all()

    return {
        "incomes": incomes,
        "expenses": expenses,
    }


def get_report_index_income_floor(moneyFormId: int, fromDate: date, toDate: date, db: Session, usr: User):

    if moneyFormId > 0:
        filterMF = Income.moneyFormId == moneyFormId
    else:
        filterMF = Floor.id > 0

    incomes = db.query(
        label("floorType", func.IF(Floor.type == 'sold', 'Patta', 'Ijara')),
        label("floorNumber", Floor.number),
        label("value", func.sum(Income.value)),
    ).select_from(Income).join(Income.client)\
        .join(Client.shop).join(Shop.floor)\
        .filter(
        func.date(Income.createdAt) >= fromDate,
        func.date(Income.createdAt) <= toDate,
        Floor.branchId == usr.branchId
    ).filter(filterMF).group_by(Floor.id).order_by(Floor.number.asc())\
        .all()

    return incomes


def get_report_index_income_contragent(moneyFormId: int, fromDate: date, toDate: date, db: Session, usr: User):

    if moneyFormId > 0:
        filterMF = Income.moneyFormId == moneyFormId
    else:
        filterMF = Contragent.id > 0

    incomes = db.query(
        label("id", Contragent.id),
        label("name", Contragent.name),
        label("value", func.sum(Income.value)),
    ).select_from(Income).join(Income.contragent)\
        .filter(
        func.date(Income.createdAt) >= fromDate,
        func.date(Income.createdAt) <= toDate,
    ).filter(filterMF).group_by(Contragent.id).order_by(Contragent.name.asc())\
        .all()

    return incomes


def get_report_index_expense_contragent(moneyFormId: int, fromDate: date, toDate: date, db: Session, usr: User):

    if moneyFormId > 0:
        filterMF = Expense.moneyFormId == moneyFormId
    else:
        filterMF = Contragent.id > 0

    expenses = db.query(
        label("id", Contragent.id),
        label("name", Contragent.name),
        label("value", func.sum(Expense.value)),
    ).select_from(Expense).join(Expense.contragent)\
        .filter(
        func.date(Expense.createdAt) >= fromDate,
        func.date(Expense.createdAt) <= toDate,
    ).filter(filterMF).group_by(Contragent.id).order_by(Contragent.name.asc())\
        .all()

    return expenses


def get_condition_branch(db: Session, usr):

    clientLoans = db.query(func.coalesce(func.sum(Client.balance), 0)).filter(
        Client.balance < 0,
    ).scalar()

    employeeSalaries = db.query(func.coalesce(func.sum(Employee.balance), 0)).filter(
        Employee.balance > 0,
    ).scalar()

    contragents = db.query(func.coalesce(func.sum(Contragent.balance), 0)).filter(
        Contragent.balance > 0,
    ).scalar()

    return {
        "clientLoans": -clientLoans,
        "employeeSalaries": employeeSalaries,
        "contragents": contragents,
    }


def get_debitor_creditor(fromYear, fromMonth, toYear, toMonth, type, db: Session, usr):

    if type == 'inner':
        return db.query(
            label("name", Client.clientName),
            label('balance', client_balance_in_month_subquery(
                fromYear, fromMonth, db)),
            label('debit', client_debet(
                fromYear, fromMonth, toYear, toMonth, db)),
            label('credit', client_credit(
                fromYear, fromMonth, toYear, toMonth, db)),
        ).all()

    elif type == 'outer':
        return db.query(
            label("name", Contragent.name),
            label('balance', contragent_balance_in_month_subquery(
                fromYear, fromMonth, db, False)),
            label('debit', contragent_debet(
                fromYear, fromMonth, toYear, toMonth, db)),
            label('credit', contragent_credit(
                fromYear, fromMonth, toYear, toMonth, db)),
        ).all()
