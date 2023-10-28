from random import randint
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import label
from app.models.floor import Floor
from app.models.moneyHistory import MoneyHistory
from app.models.user import User
import calendar

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

def get_income(floor_id: int, _year: int, _month: int, db:Session):

    yearlyIncome = 0

    if floor_id > 0:
        floorFilter = MoneyHistory.floorId == floor_id
    else:
        floorFilter = MoneyHistory.id > 0

    if _month == 0:
        incomes = db.query(
            label("value", func.sum(MoneyHistory.value)),
            label("month", func.month(MoneyHistory.createdAt)),
        ).filter(
            func.year(MoneyHistory.createdAt) == _year,
            MoneyHistory.branchId==1,
            MoneyHistory.value > 0
        ).filter(floorFilter).order_by(
            func.month(MoneyHistory.createdAt).asc()
        ).group_by(
            func.month(MoneyHistory.createdAt)
        ).all()

        rangeList = range(1, MONTHS_COUNT+1)

    else:

        incomes = db.query(
            label("value", func.sum(MoneyHistory.value)),
            label("month", func.DAY(MoneyHistory.createdAt)),
        ).filter(
            func.month(MoneyHistory.createdAt) == _month,
            func.year(MoneyHistory.createdAt) == _year,
            MoneyHistory.floorId == floor_id,
            MoneyHistory.branchId==1,
            MoneyHistory.value > 0
        ).order_by(
            func.DAY(MoneyHistory.createdAt).asc()
        ).group_by(
            func.DAY(MoneyHistory.createdAt)
        ).all()

        rangeList = range(1, calendar.monthrange(_year, _month)[1]+1)

    incomesByMonths = []

    for month in rangeList:

        isFound = False

        for income in incomes:
            if month == income.month:

                incomesByMonths.append({
                    'monthName': MONTHS[month] if _month == 0 else str(month),
                    'value': income.value
                })

                incomesByMonths.append(income)
                yearlyIncome += income.value
                isFound = True

        if isFound == False:
            incomesByMonths.append({
                'monthName': MONTHS[month] if _month == 0 else str(month),
                'value': randint(2000000, 90000000),
            })
    return {
        "incomesByMonths": incomesByMonths,
        "yearlyIncome": yearlyIncome
    }