from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.parkingCar import *
from app.schemas.parkingCar import *
from app.utils.handler import integrityHandler
from app.utils.pagination import pagination
import math

def get_all_parkingCars(search, page, limit, usr, db: Session):

    parkingCars = db.query(ParkingCar)

    # if search:
    # parkingCars = parkingCars.filter(
    # ParkingCar.name.like(f"%{search}%"),
    # )

    return pagination(parkingCars, page, limit)


def enter_parkingCar(form_data: NewParkingCar, usr, db: Session):

    try:

        parkingZone: ParkingZone = db.get(ParkingZone, form_data.parkingZoneId)
        if not parkingZone:
            raise HTTPException(400, "Parkovka topilmadi")
        

        new_parkingCar = ParkingCar(
            number=form_data.number,
            hourlyFee=parkingZone.hourlyFee,
            parkingZoneId=parkingZone.id,
            enteredAt=form_data.enteredAt,
        )

        db.add(new_parkingCar)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        integrityHandler(e)


def exit_parkingCar(form_data: UpdateParkingCar, usr, db: Session):

    try:
        parkingCar: ParkingCar = db.query(ParkingCar).filter(
            ParkingCar.number == form_data.number, 
            ParkingCar.exitedAt == None,

        ).order_by(ParkingCar.enteredAt.desc()).first()
        
        if parkingCar:

            if form_data.exitedAt <= parkingCar.enteredAt:
                raise HTTPException(status_code=400, detail="So`rovda xatolik!")
            else:
                parkingSeconds = parkingCar.enteredAt - form_data.exitedAt
                parkingCeiledHours = math.ceil(parkingSeconds / 60 / 60)

                parkingCar.totalFee = parkingCeiledHours * parkingCar.hourlyFee
                parkingCar.exitedAt = form_data.exitedAt

                db.commit()

                raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
