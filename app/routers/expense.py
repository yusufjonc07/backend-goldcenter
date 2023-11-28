from click import Option
from fastapi import Body, HTTPException, APIRouter, Depends, UploadFile, File
from typing import Optional

from pydantic import Field
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
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_expenses(search, expenseType, fromDate, toDate, employeeId,  page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@expense_router.post("/expense/create")
async def create_new_income(
    type: ExpenceTypes = Body(...),
    employeeId: Optional[int] = Body(0),
    value: float = Body(..., gt=0),
    moneyFormId: int = Body(...),
    comment: str = Body(..., min_length=5),
    file: UploadFile = File(...),
    floorId: Optional[int] = Body(0),
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):

    if not usr.userRole in ['any_role']:
        try:

            isProceed = False

            fileName = await validate_file(file, ['document', 'image'], 3)

            if type == 'salary':
                employee = db.get(Employee, employeeId)

                if not employee:
                    raise HTTPException(400, "Mijoz shartnomasi topilmadi")
                else:
                    employee.balance -= value
                    db.flush()

            isProceed = True

            if isProceed:
                new_expense = Expense(
                    type=type,
                    employeeId=employeeId if employeeId > 0 else None,
                    value=value,
                    moneyFormId=moneyFormId,
                    floorId=floorId if floorId > 0 else None,
                    branchId=usr.branchId,
                    comment=comment,
                    userId=usr.id,
                    fileName=fileName,
                )
            db.add(new_expense)
            db.commit()

            await save_file(file, fileName, f"expenses")

            raise HTTPException(200, "Ma`lumotlar saqlandi!")
        except IntegrityError as e:
            raise HTTPException(400, e.args)
            # raise integrityHandler(e)
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
