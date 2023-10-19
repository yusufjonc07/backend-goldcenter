import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.message import *
from app.schemas.message import *


def get_all_messages(search, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    messages = db.query(Message)

    # if search:
    # messages = messages.filter(
    # Message.id.like(f"%{search}%"),
    # )

    all_data = messages.order_by(Message.id.desc()).offset(offset).limit(limit)
    count_data = messages.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }


def create_message(form_data: NewMessage, usr, db: Session):

    try:
        new_message = Message(
            type=form_data.type,
            userId=form_data.userid,
            forRole=form_data.forrole,
            branchId=form_data.branchid,
            replyId=form_data.replyid,
            createdAt=form_data.createdat,
            updated_at=form_data.updated_at,
        )

        db.add(new_message)
        db.commit()

        return new_message
    except IntegrityError as e:
        raise HTTPException(400, e.args)


def update_message(id, form_data: UpdateMessage, usr, db: Session):

    try:
        message = db.query(Message).filter(Message.id == id)
        this_message = message.first()
        if this_message:
            message.update({
                Message.type: form_data.type,
                Message.userId: form_data.userid,
                Message.forRole: form_data.forrole,
                Message.branchId: form_data.branchid,
                Message.replyId: form_data.replyid,
                Message.createdAt: form_data.createdat,
                Message.updated_at: form_data.updated_at,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
