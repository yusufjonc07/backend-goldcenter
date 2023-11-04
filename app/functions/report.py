from datetime import date
from random import randint
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import label
from app.models.clientAgreement import ClientAgreement
from app.models.floor import Floor
from app.models.expense import Expense
from app.models.income import Income
from app.models.shop import Shop
from app.models.user import User
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
            Floor.branchId == 1,
            Income.value > 0
        ).join(Income.clientAgreement).join(ClientAgreement.shop).join(Shop.floor)
        
        if floor_id > 0:
            incomes = incomes.join(Income.clientAgreement)\
                .join(ClientAgreement.shop).filter(Shop.floorId==floor_id)

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
            Shop.floorId == floor_id,
            Floor.branchId == 1,
            Income.value > 0
        ).join(Income.clientAgreement).join(ClientAgreement.shop).join(Shop.floor).order_by(
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
                    'value': income.value,
                })

                yearlyIncome += income.value

       

    return {
        "incomesByMonths": incomesByMonths,
        "yearlyIncome": yearlyIncome
    }

def get_report_index(fromDate: date, toDate: date, db: Session, usr: User):

    pas = ''
