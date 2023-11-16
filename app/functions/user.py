import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.user import *
from app.schemas.user import *
from app.utils.handler import integrityHandler
from security.auth import get_password_hash


def get_all_users(search, employeeId, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    users = db.query(User)

    if employeeId > 0:
        users = users.filter(User.employeeId==employeeId)

    # if search:
    # users = users.filter(
    # User.id.like(f"%{search}%"),
    # )

    all_data = users.order_by(User.id.desc()).offset(offset).limit(limit)
    count_data = users.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }


def create_user(form_data: NewUser, usr: User, db: Session):

    try:

        employee = db.get(Employee, form_data.employeeid)

        if not employee:
            raise HTTPException(400, 'Hodim topilmadi')

        new_user = User(
            employeeId=form_data.employeeid,
            username=form_data.username,
            userRole=employee.role,
            passwordHash=get_password_hash(form_data.password),
            branchId=usr.branchId,
        )

        db.add(new_user)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise integrityHandler(e)


def update_user(id, form_data: UpdateUser, usr, db: Session):

    try:
        user = db.query(User).filter(User.id == id)
        this_user = user.first()
        if this_user:

            if len(form_data.password) > 5:
                passwordHash = get_password_hash(form_data.password)
            else:
                passwordHash = this_user.passwordHash

            user.update({
                "userRole": form_data.userrole,
                "username": form_data.username,
                "passwordHash": passwordHash,
                "disabled": form_data.disabled,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
