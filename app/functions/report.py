from random import randint
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import label
from app.models.floor import Floor
from app.models.moneyHistory import MoneyHistory
from app.models.user import User
from datetime import date

from app.schemas.enums import ReportTypes

MONTHS_COUNT = 12
MONTHS = {
    1:'Yanvar',
    2:'Fevral',
    3:'Mart',
    4:'Aprel',
    5:'May',
    6:'Iyun',
    7:'Iyul',
    8:'Avgust',
    9:'Sentabr',
    10:'Oktabr',
    11:'Noyabr',
    12:'Dekabr',
}

def get_yearly_income(floor_id: int, type: ReportTypes, usr: User, db:Session):
    total_income = 0
    incomes = db.query(
        label("value", func.sum(MoneyHistory.value)),
        label("label", func.year(MoneyHistory.createdAt)),
    ).filter(
        MoneyHistory.floorId == floor_id,
        MoneyHistory.value > 0
    ).order_by(
        func.year(MoneyHistory.createdAt).asc()
    ).group_by(
        func.year(MoneyHistory.createdAt)
    ).all()

    incomesByYears = []

    for year in range(2023, 2033):

        isFound = False
        for income in incomes:
            if year == income.label:
                incomesByYears.append(income)
                yearlyIncome += income.value
                isFound = True

        if isFound == False:
            incomesByYears.append({
                "value": randint(2000000, 90000000),
                "label": year
            })

    for m in incomesByYears:
        m['labelName'] = MONTHS[m['label']]
        del m['label']

    return {
        "incomesData": incomesByYears,
        "totalIncome": total_income
    }

def get_income(floor_id: int, type: ReportTypes, usr: User, db:Session):

    yearlyIncome = 0

    incomes = db.query(
        label("value", func.sum(MoneyHistory.value)),
        label("month", func.month(MoneyHistory.createdAt)),
    ).filter(
        func.year(MoneyHistory.createdAt) == date.year,
        MoneyHistory.floorId == floor_id,
        MoneyHistory.value > 0
    ).order_by(
        func.month(MoneyHistory.createdAt).asc()
    ).group_by(
        func.month(MoneyHistory.createdAt)
    ).all()

    incomesByMonths = []

    for month in range(1, MONTHS_COUNT+1):

        isFound = False

        for income in incomes:
            if month == income.month:
                incomesByMonths.append(income)
                yearlyIncome += income.value
                isFound = True

        if isFound == False:
            incomesByMonths.append({
                "value": randint(2000000, 90000000),
                "month": month
            })

    for m in incomesByMonths:
        m['monthName'] = MONTHS[m['month']]
        del m['month']

    return {
        "incomesByMonths": incomesByMonths,
        "yearlyIncome": yearlyIncome
    }