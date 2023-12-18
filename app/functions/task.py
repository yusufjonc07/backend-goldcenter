import math
from sqlalchemy.orm import aliased, Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.task import *
from app.schemas.task import *
from sqlalchemy.sql import label, or_
from app.utils.pagination import pagination


CHAT_ROLES = ["headConstructor", "headGuard", "headCleaner", "accountant"]


def get_all_tasks(search, isOnlyUnread, page, limit, usr, db: Session):

    tasks = db.query(Task).options(
        joinedload(Task.employee),
        joinedload(Task.responseEmployee),
    )

    return pagination(tasks, page, limit)


def create_task(form_data: NewTask, usr: User, db: Session):

    try:
        new_task = Task(
            context=form_data.context,
            type=form_data.type,
            userId=usr.id,
            forRole=form_data.forrole,
            branchId=usr.branchId,
            replyId=(form_data.replyid if form_data.replyid >
                     0 else text("NULL")),
        )

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return new_task

    except IntegrityError as e:
        raise HTTPException(400, e.args)


def update_task(id, form_data: UpdateTask, usr, db: Session):

    try:
        task = db.query(Task).filter(Task.id == id)
        this_task = task.first()
        if this_task:
            task.update({
                Task.type: form_data.type,
                Task.userId: form_data.userid,
                Task.forRole: form_data.forrole,
                Task.branchId: form_data.branchid,
                Task.replyId: form_data.replyid,
                Task.createdAt: form_data.createdat,
                Task.updated_at: form_data.updated_at,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
