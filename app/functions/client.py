import math
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.client import *
from app.schemas.client import *


def get_all_clients(search, page, limit, usr, db: Session):
    if page == 1 or page < 1:
        offset = 0
    else:
        offset = (page-1) * limit

    clients = db.query(Client)

    # if search:
    # clients = clients.filter(
    # Client.id.like(f"%{search}%"),
    # )

    all_data = clients.order_by(Client.id.desc()).offset(offset).limit(limit)
    count_data = clients.count()

    return {
        "data": all_data.all(),
        "page_count": math.ceil(count_data / limit),
        "data_count": count_data,
        "current_page": page,
        "page_limit": limit,
    }


def create_client(form_data: NewClient, usr, db: Session):

    try:
        new_client = Client(
            firstname=form_data.firstname,
            lastname=form_data.lastname,
            phoneNumber=form_data.phonenumber,
            passportSeriaNumber=form_data.passportserianumber,
            inn=form_data.inn,
        )

        db.add(new_client)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise HTTPException(400, "Bu ismli mijoz mavjud")

def update_client(id, form_data: UpdateClient, usr, db: Session):

    try:
        client = db.query(Client).filter(Client.id == id)
        this_client = client.first()
        if this_client:
            client.update({
                Client.firstname: form_data.firstname,
                Client.lastname: form_data.lastname,
                Client.phoneNumber: form_data.phonenumber,
                Client.passportSeriaNumber: form_data.passportserianumber,
                Client.inn: form_data.inn,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
