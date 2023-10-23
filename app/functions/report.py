from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import label
from app.models.moneyHistory import Moneyhistory
from app.models.user import User
from datetime import date


def get_income(floor_id: int, usr: User, db:Session):
    
    incomes = db.query(
        label("value", func.sum(Moneyhistory.value)),
        label("month", func.month(Moneyhistory.createdAt)),
    ).filter(
        func.year(Moneyhistory.createdAt) == date.year,
        Moneyhistory.floorId == floor_id,
        Moneyhistory.value > 0
    ).order_by(func.month(Moneyhistory.createdAt).asc()).group_by(func.month(Moneyhistory.createdAt)).all()

    incomesByMonths = []

    for month in range(1, 13):

        st = False

        for income in incomes:
            if month == income.month:
                incomesByMonths.append(income)
                st = True

        if st == False:
            incomesByMonths.append({
                "value": 0,
                "month": month
            })

    return incomesByMonths