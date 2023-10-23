from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import label
from app.models.floor import Floor
from app.models.moneyHistory import Moneyhistory
from app.models.user import User
from datetime import date

MONTHS_COUNT = 12

def get_income(floor_id: int, usr: User, db:Session):

    if not db.get(Floor, floor_id):
        raise HTTPException(400, "Qavat topilmadi.")

    yearlyIncome = 0

    incomes = db.query(
        label("value", func.sum(Moneyhistory.value)),
        label("month", func.month(Moneyhistory.createdAt)),
    ).filter(
        func.year(Moneyhistory.createdAt) == date.year,
        Moneyhistory.floorId == floor_id,
        Moneyhistory.value > 0
    ).order_by(
        func.month(Moneyhistory.createdAt).asc()
    ).group_by(
        func.month(Moneyhistory.createdAt)
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