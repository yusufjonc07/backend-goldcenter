from cProfile import label
import math
from sqlalchemy.orm import subqueryload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.message import *
from app.schemas.message import *
from sqlalchemy.sql import label, or_

CHAT_ROLES = ["headConstructor", "headGuard", "headCleaner", "accountant"]

def get_all_messages(search, isOnlyUnread, page, limit, usr, db: Session):
    
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit



    messages = db.query(
        label('id', Message.id),
        label('fileName', Message.fileName),
        label('context', Message.context),
        label('createdAt', Message.createdAt),
        label('isViewed', Message.isViewed),
        label('forRole', Message.forRole),
        label('replyId', Message.replyId),
        label('updated_at', Message.updated_at),
        label('employeeName', func.concat(Employee.lastname, ' ', Employee.firstname)),
        label('employeeRole', Employee.role),
    ).join(Message.user).join(User.employee).filter(Message.type == 'request')


    if isOnlyUnread == True:

        messages = messages.filter(Message.isViewed==False)

        if usr.userRole in CHAT_ROLES:
            messages = messages.filter(Message.forRole==usr.userRole)
    else:
        if usr.userRole in CHAT_ROLES:
            messages = messages.filter(
                or_(
                    Message.forRole==usr.userRole,
                    Message.userId==usr.Id
                )
            )


    # if search:
    # messages = messages.filter(
    # Message.id.like(f"%{search}%"),
    # )

    all_data = messages.order_by(Message.id.desc()).offset(offset).limit(limit)
    count_data = messages.count()

    data_all = []

    for data_one in all_data.all():
        data_item = dict(data_one)
        data_item['replies'] = db.query(
            label('id', Message.id),
            label('fileName', Message.fileName),
            label('context', Message.context),
            label('createdAt', Message.createdAt),
            label('isViewed', Message.isViewed),
            label('forRole', Message.forRole),
            label('replyId', Message.replyId),
            label('updated_at', Message.updated_at),
            label('type', Message.type),
            # label('employeeName', func.concat(Employee.lastname, ' ', Employee.firstname)),
            # label('employeeRole', Employee.role),
        ).filter(Message.replyId==data_one.id).all()

        data_all.append(data_item)

    return {
        "data": data_all,
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }


def create_message(form_data: NewMessage, usr: User, db: Session):

    try:
        new_message = Message(
            context=form_data.context, 
            type=form_data.type,
            userId=usr.id,
            forRole=form_data.forrole,
            branchId=usr.branchId,
            replyId=(form_data.replyid if form_data.replyid > 0 else text("NULL")),
        )

        db.add(new_message)
        db.commit()
        db.refresh(new_message)

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
