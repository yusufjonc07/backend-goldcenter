import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from typing import List
from app.models.income import *
from app.schemas.income import *
from app.utils.handler import integrityHandler
from app.utils.pagination import pagination


def get_all_incomes(search, page, limit, usr, db: Session):

    incomes = db.query(Income)

    # if search:
    # incomes = incomes.filter(
    # Income.id.like(f"%{search}%"),
    # )

    return pagination(incomes, page, limit)


def get_last_electrAmount(id: int, db: Session):
    return db.query(Income).filter_by(
        clientId=id, type='utility'
    ).order_by(Income.electrLastAmount).first()


def create_income(form_datas: List[NewIncome], usr, db: Session):
    try:
        for form_data in form_datas:

            new_income = Income(
                clientId=form_data.clientId if form_data.clientId > 0 else None,
                regularIncomeId=form_data.regularIncomeId if form_data.regularIncomeId > 0 else None,
                value=form_data.value,
                moneyFormId=form_data.moneyFormId,
                comment=form_data.comment,
                type=form_data.type,
                forMonth=form_data.forMonth,
                forYear=form_data.forYear,
                userId=usr.id,
            )

            db.add(new_income)
            db.flush()
            db.refresh(new_income)

            if form_data.clientId > 0:
                new_income.client.balance += new_income.value

            new_income.moneyForm.balance += new_income.value

        db.commit()
        raise HTTPException(status_code=200, detail="Ma'lumotlar saqlandi!")

    except IntegrityError as e:
        raise integrityHandler(e)


def update_income(id, form_data: UpdateIncome, usr, db: Session):

    try:
        income = db.query(Income).filter(Income.id == id)
        this_income = income.first()
        if this_income:
            income.update({
                Income.clientId: form_data.clientId,
                Income.value: form_data.value,
                Income.moneyFormId: form_data.moneyFormId,
                Income.comment: form_data.comment,
                Income.type: form_data.type,
                Income.forMonth: form_data.forMonth,
                Income.forYear: form_data.forYear,
                Income.userId: usr.id,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)


def validate_clients_by_inn(client_inns, db: Session):

    unique_client_inns = list(set(client_inns))
    not_found_inns = []

    # validate
    for inn in unique_client_inns:
        client = db.query(Client).filter_by(inn=inn).first()
        if not client:
            not_found_inns.append(inn)

    if len(not_found_inns) > 0:
        raise HTTPException(400, ", ".join(not_found_inns) +
                            ". Bu INN lardagi mijozlar topilmadi!")

    return True


def validate_money_forms_by_name(money_form_names, db: Session):

    unique_money_form_names = list(set(money_form_names))
    not_found_names = []

    for name in unique_money_form_names:
        money_form = db.query(Moneyform).filter_by(name=name).first()
        if not money_form:
            not_found_names.append(name)

    if len(not_found_names) > 0:
        raise HTTPException(400, ", ".join(not_found_names) +
                            ". Bu nomlardagi kassalar topilmadi!")

    return True


def validate_excel_ws(worksheet, db: Session):

    # inn array
    client_inns = []

    # money form array
    money_form_names = []

    # get first 1000 rows from worksheet
    for row in worksheet.iter_rows(min_row=2, max_col=7, max_row=1000):

        # stop a loop when the cell is empty
        if row[0].value is None:
            break

        client_inns.append(str(row[0].value))
        money_form_names.append(str(row[2].value))

    validate_clients_by_inn(client_inns, db)
    validate_money_forms_by_name(money_form_names, db)


def create_income_by_ecxel_data(excel_datas: List[NewIncomeExcel], db: Session, usr: User):

    income_form_datas = []

    for excel_data in excel_datas:

        client = db.query(Client).filter_by(inn=excel_data.inn).first()
        moneyForm = db.query(Moneyform).filter_by(
            name=excel_data.moneyFormName).first()

        income_form_datas.append(NewIncome(
            clientId=client.id,
            value=excel_data.value,
            moneyFormId=moneyForm.id,
            createdAt=excel_data.date,
            type=excel_data.type,
            forYear=excel_data.forYear,
            forMonth=excel_data.forMonth,
        ))

    create_income(income_form_datas, usr, db)
