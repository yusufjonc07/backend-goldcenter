from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.debetHistory import *
from app.schemas.debetHistory import *
from app.utils.handler import integrityHandler
from app.utils.pagination import pagination


def get_all_debetHistorys(search, contragentId, page, limit, usr, db: Session):

    debetHistorys = db.query(DebetHistory)

    if search:
        debetHistorys = debetHistorys.filter(
            DebetHistory.comment.like(f"%{search}%"),
        )

    if contragentId > 0:
        debetHistorys = debetHistorys.filter(
            DebetHistory.contragentId == contragentId,
        )

    return pagination(debetHistorys, page, limit)


def create_debetHistory(form_data: NewDebethistory, usr, db: Session):

    try:
        new_debetHistory = DebetHistory(
            comment=form_data.comment,
            contragentId=form_data.contragentId,
            value=form_data.value,
        )

        db.add(new_debetHistory)

        regExpense = db.get(
            Contragent, form_data.contragentId)

        if not regExpense:
            raise HTTPException(
                400, f"Doimiy chiqim topilmadi")
        else:
            regExpense.balance += form_data.value
            db.flush()

        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        integrityHandler(e)


def update_debetHistory(id, form_data: UpdateDebethistory, usr, db: Session):

    try:
        debetHistory = db.query(DebetHistory).filter(DebetHistory.id == id)
        this_debetHistory = debetHistory.first()
        if this_debetHistory:
            debetHistory.update({
                DebetHistory.comment: form_data.comment,
                DebetHistory.contragentId: form_data.contragentId,
                DebetHistory.value: form_data.value,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
