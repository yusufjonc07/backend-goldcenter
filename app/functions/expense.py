import math
from sqlalchemy.orm import aliased, Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.expense import *
from app.schemas.expense import *
from sqlalchemy.sql import label

def get_all_expenses(search, type, employeeId, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit
    
    worker_alias = aliased(Employee, name='worker_alias')

    worker = db.query(func.concat(worker_alias.firstname, ' ', worker_alias.lastname)).filter_by(id=Expense.employeeId).subquery()
    
    expenses = db.query(
        label('type', Expense.type),    
        label('worker', worker),    
        label('comment', Expense.comment),    
        label('user', func.concat(Employee.firstname, ' ', Employee.lastname)),    
        label('createdAt', Expense.createdAt),    
        label('value', Expense.value),    
        label('moneyForm', Moneyform.name),    
    ).join(Expense.user).join(User.employee).join(Expense.moneyForm)
        
    if type:
       expenses = expenses.filter(Expense.type==type)

    # if search:
    # expenses = expenses.filter(
    # Expense.id.like(f"%{search}%"),
    # )

    all_data = expenses.order_by(
        Expense.id.desc()).offset(offset).limit(limit)
    count_data = expenses.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }


def create_expense(form_data: NewExpense, usr, db: Session):
    
    try:
        new_expense = Expense(
            type=form_data.type,
        employeeId=form_data.employeeid,
        value=form_data.value,
        moneyFormId=form_data.moneyformid,
        comment=form_data.comment,
        userId=form_data.userid,
        fileName=form_data.filename,
        createdAt=form_data.createdat,
        branchId=form_data.branchid,
        floorId=form_data.floorid,
    )

        db.add(new_expense)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)

def update_expense(id, form_data: UpdateExpense, usr, db: Session):
    
    try:
        expense = db.query(Expense).filter(Expense.id == id)
        this_expense = expense.first()
        if this_expense:
            expense.update({    
            Expense.type: form_data.type,
            Expense.employeeId: form_data.employeeid,
            Expense.value: form_data.value,
            Expense.moneyFormId: form_data.moneyformid,
            Expense.comment: form_data.comment,
            Expense.userId: form_data.userid,
            Expense.fileName: form_data.filename,
            Expense.createdAt: form_data.createdat,
            Expense.branchId: form_data.branchid,
            Expense.floorId: form_data.floorid,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
    
