from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import Session
from app.models.contragent import *
from app.models.income import *
from app.functions.contragent import *
from app.schemas.contragent import *
from sqlalchemy.sql import label
from datetime import datetime

contragent_router = APIRouter(tags=['Kontragent Endpoint'])


@contragent_router.get("/contragents", description="This router returns list of the contragents using pagination")
async def get_contragents_list(
    search: Optional[str] = "",
    category_id: Optional[int] = 0,
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_contragents(search, category_id, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@contragent_router.get("/contragent/{id}/akt-sverka")
async def get_contragent_akt_sverka(
    id: int,
    year: int,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        contragent: Contragent = db.get(Contragent, id)
        if contragent:

            contragent = db.query(Contragent, label("monthBeginBalance",
                                                    contragent_balance_in_month_subquery(year, 1, db, end=False))
                                  ).filter(Contragent.id == id).first()

            data = []

            fees = db.query(DebetHistory).filter(
                DebetHistory.contragentId == id,
                func.year(DebetHistory.createdAt) == year,
            ).all()

            for fee in fees:
                data.append({
                    "type": "fee",
                    "date": datetime.strptime(fee.createdAt.strftime("%Y-%m-%d"), "%Y-%m-%d"),
                    "value": fee.value,
                    "comment": fee.comment,
                    "moneyForm": None,
                })

            incomes = db.query(Income).filter(
                Income.contragentId == id,
                func.year(Income.createdAt) == year,
            ).all()

            for income in incomes:
                data.append({
                    "type": "income",
                    "date": datetime.strptime(income.createdAt.strftime("%Y-%m-%d"), "%Y-%m-%d"),
                    "value": income.value,
                    "comment": income.comment,
                    "moneyForm": income.moneyForm.name,
                })

            expenses = db.query(Expense).filter(
                Expense.contragentId == id,
                func.year(Expense.createdAt) == year,
            ).all()

            for expense in expenses:
                data.append({
                    "type": "expense",
                    "date": datetime.strptime(expense.createdAt.strftime("%Y-%m-%d"), "%Y-%m-%d"),
                    "value": expense.value,
                    "comment": expense.comment
                })

            sorted_data = sorted(data, key=lambda x: x['date'])

            return {
                "contragent": contragent,
                "data": sorted_data,
            }

        else:
            raise HTTPException(
                status_code=400, detail="Bunday mijoz mavjud emas!")

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@contragent_router.post("/contragent/create", description="This router is able to add new contragent")
async def create_new_contragent(
    form_data: NewContragent,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_contragent(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@contragent_router.put("/contragent/{id}/update", description="This router is able to update contragent")
async def update_one_contragent(
    id: int,
    form_data: UpdateContragent,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_contragent(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@contragent_router.delete("/contragent/{id}/delete")
async def delete_one_contragent(
    id: int,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return delete_contragent(id, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
