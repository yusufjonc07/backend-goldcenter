from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.parkingZone import *
from app.schemas.parkingZone import *
from app.utils.handler import integrityHandler
from app.utils.pagination import pagination


def get_all_parkingZones(search, page, limit, usr, db: Session):

    parkingZones = db.query(ParkingZone)

    # if search:
    # parkingZones = parkingZones.filter(
    # ParkingZone.name.like(f"%{search}%"),
    # )

    return pagination(parkingZones, page, limit)


def create_parkingZone(form_data: NewParkingZone, usr, db: Session):

    try:
        new_parkingZone = ParkingZone(
            name=form_data.name,
            hourlyFee=form_data.hourlyfee,
            branchId=usr.branchId,
        )

        db.add(new_parkingZone)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        integrityHandler(e)


def update_parkingZone(id, form_data: UpdateParkingZone, usr, db: Session):

    try:
        parkingZone = db.query(ParkingZone).filter(ParkingZone.id == id)
        this_parkingZone = parkingZone.first()
        if this_parkingZone:
            parkingZone.update({
                ParkingZone.name: form_data.name,
                ParkingZone.hourlyFee: form_data.hourlyfee,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
