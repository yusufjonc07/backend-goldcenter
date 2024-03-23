from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.branch import *
from app.models.client import *
from app.models.attandance import *
from app.models.clientFee import *
from app.models.document import *
from app.models.expense import *
from app.models.income import *
from app.models.notification import *
from app.models.parkingCar import *
from app.models.regularExpence import *
from app.models.salary import *
from app.models.task import *
from app.schemas.branch import *
from app.utils.fileUtil import delete_files_in_folder, delete_folder
from app.utils.pagination import pagination


def get_all_branchs(search, page, limit, usr, db: Session):

    branchs = db.query(Branch)

    # if search:
    # branchs = branchs.filter(
    # Branch.id.like(f"%{search}%"),
    # )

    return pagination(branchs, page, limit)


def create_branch(form_data: NewBranch, usr, db: Session):

    try:
        new_branch = Branch(
            name=form_data.name,
            address=form_data.address,
            dollar=form_data.dollar,
            electrPrice=form_data.electrPrice,
        )

        db.add(new_branch)
        db.commit()

        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)


def update_branch(id, form_data: UpdateBranch, usr, db: Session):

    try:
        branch = db.query(Branch).filter(Branch.id == id)
        this_branch = branch.first()
        if this_branch:
            branch.update({
                Branch.name: form_data.name,
                Branch.address: form_data.address,
                Branch.dollar: form_data.dollar,
                Branch.electrPrice: form_data.electrPrice,
            })
            db.commit()

            raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
        else:
            raise HTTPException(status_code=400, detail="So`rovda xatolik!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)


def delete_practices(usr, db: Session):

    try:

        # db.query(Attandance).delete()
        db.query(ClientFee).delete()
        db.query(Document).delete()
        db.query(Expense).delete()
        db.query(Income).delete()
        db.query(Notification).delete()
        db.query(ParkingCar).delete()
        db.query(RegularExpence).delete()
        db.query(Salary).delete()
        db.query(Task).delete()

        db.query(Client).update({
            Client.balance: 0
        })

        delete_files_in_folder('documents')
        delete_files_in_folder('expenses')
        delete_folder('headCleaner')
        delete_folder('headConstructor')
        delete_folder('headGuard')

        db.commit()

        raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
    except IntegrityError as e:
        raise HTTPException(400, e.args)
