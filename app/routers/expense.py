from click import Option
from fastapi import Body, HTTPException, APIRouter, Depends, UploadFile, File, Form
from typing import Optional, List
import json

from pydantic import ValidationError
from app.models.regularExpence import Regularexpence
from app.schemas.user import NewUser
from app.utils.fileUtil import save_file, validate_file
from app.utils.handler import integrityHandler
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import Session
from app.models.expense import *
from app.functions.expense import *
from app.schemas.expense import *
from datetime import date

expense_router = APIRouter(tags=['Kassa Endpoint'])


@expense_router.get("/expenses", description="This router returns list of the expenses using pagination")
async def get_expenses_list(
    search: Optional[str] = "",
    expenseType: Optional[ExpenceTypes] = None,
    fromDate: Optional[date] = None,
    toDate: Optional[date] = None,
    employeeId: Optional[int] = 0,
    regularExpenceId: Optional[int] = 0,
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_expenses(search, expenseType, fromDate, toDate, employeeId, regularExpenceId,  page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@expense_router.post("/expense/create")
async def create_new_income(
    form_data_string: str = Form(...,
                                 description="Bu yerga string kelishi kerak"),
    file: Optional[UploadFile] = File("none"),
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):

    """
        `form_data_string`
        [
            {
                "type": "salary",
                "employeeId": 12,
                "regularExpenceId": 0,
                "value": 1,
                "moneyFormId": 1,
                "comment": "string"
            }
        ]
    """

    if not usr.userRole in ['any_role']:

        try:
            form_datas_dict = json.loads(form_data_string)
        except Exception as err:
            raise HTTPException(
                422, f"form_data_string xato jo'natildi: {err.args}")

        if type(form_datas_dict).__name__ != 'list':
            raise HTTPException(
                422, "form_data_string - list emas, object kelyapti")

        form_datas = []
        for form_data_dict in form_datas_dict:
            try:
                form_datas.append(
                    NewExpense(**form_data_dict)
                )
            except ValidationError as vErr:
                raise HTTPException(422, vErr.errors())

        if file != 'none':
            fileName = await validate_file(file, ['document', 'image'], 3)
        else:
            fileName = None

        for form_data in form_datas:

            if form_data.type == 'salary':
                employee = db.get(Employee, form_data.employeeId)

                if not employee:
                    raise HTTPException(400, "Hodim topilmadi topilmadi")
                else:
                    employee.balance -= form_data.value
                    db.flush()

            if form_data.type == 'regular':
                regExpense = db.get(
                    Regularexpence, form_data.regularExpenceId)

                if not regExpense:
                    raise HTTPException(
                        400, f"Doimiy chiqim topilmadi")
            try:
                new_expense = Expense(
                    type=form_data.type,
                    employeeId=form_data.employeeId if form_data.employeeId > 0 else None,
                    regularExpenceId=form_data.regularExpenceId if form_data.regularExpenceId > 0 else None,
                    value=form_data.value,
                    moneyFormId=form_data.moneyFormId,
                    branchId=usr.branchId,
                    comment=form_data.comment,
                    userId=usr.id,
                    fileName=fileName,
                )
                db.add(new_expense)
                db.flush()
            except IntegrityError as e:
                raise integrityHandler(e)

        if fileName:
            await save_file(file, fileName, f"expenses")

        new_expense.moneyForm.balance -= new_expense.value

        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@expense_router.put("/expense/{id}/update", description="This router is able to update expense")
async def update_one_expense(
    id: int,
    form_data: UpdateExpense,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_expense(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
