from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import label
from app.models.floor import Floor
from app.models.moneyHistory import MoneyHistory
from app.models.user import User
from datetime import date

MONTHS_COUNT = 12

def get_income(floor_id: int, usr: User, db:Session):

    if not db.get(Floor, floor_id):
        raise HTTPException(400, "Qavat topilmadi.")

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
                "value": 0,
                "month": month
            })

    return {
        "incomesByMonths": incomesByMonths,
        "yearlyIncome": yearlyIncome
    }