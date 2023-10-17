import math
from fastapi import APIRouter, Depends, HTTPException
from databases.main import Base, ActiveSession
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import Optional
from enum import Enum

from security.auth import get_current_active_user


class Ingonarables(str, Enum):
    list = "list"
    view = "view"
    update = "update"
    delete = 'delete'


class Addable(str, Enum):
    pass


class Resource(APIRouter):

    def __init__(
        self,
        name: str,
        modelClass: Base,
        createForm: BaseModel,
        editForm: Optional[BaseModel] = None,
        ignorables=[Ingonarables],
        tags=[]
    ):

        super().__init__(tags=tags, prefix=f"/{name}")

        if not editForm:
            editForm = createForm

        if not "list" in ignorables:
            @self.get("")
            async def get_all(
                    page: int = 1,
                    limit: int = 10,
                    db: Session = ActiveSession,
                    usr: any = Depends(get_current_active_user)):

                try:

                    if page == 1 or page < 1:
                        offset = 0
                    else:
                        offset = (page-1) * limit

                    query = db.query(modelClass)

                    return {
                        "data": query.order_by(modelClass.id.desc()).offset(offset).limit(limit).all(),
                        "count": math.ceil(query.count() / limit),
                        "page": page,
                        "limit": limit,
                    }
                
                except IntegrityError:
                    return HTTPException(400, 'Something went wrong')
                except Exception:
                    return HTTPException(400, 'Internal server error')

        if not "create" in ignorables:
            @self.post("/create")
            async def create_one(form_data: createForm, db: Session = ActiveSession):

                try:
                    new_model = modelClass(**form_data)
                    db.add(new_model)
                    db.commit()

                    return new_model

                except IntegrityError:
                    return HTTPException(400, 'Something went wrong')
                except Exception:
                    return HTTPException(400, 'Internal server error')

        if not "view" in ignorables:
            @self.get("/{id}")
            async def get_one(id: int, db: Session = ActiveSession):

                try:

                    record = db.get(modelClass, id)
                    if not record:
                        raise HTTPException(400, "Record was not found")

                    return record

                except IntegrityError:
                    return HTTPException(400, 'Something went wrong')
                except Exception:
                    return HTTPException(400, 'Internal server error')

        @self.put("/update/{id}")
        async def update_one(id: int, form_data: editForm, db: Session = ActiveSession):

            try:

                record = db.get(modelClass, id)
                if not record:
                    raise HTTPException(400, "Record was not found")

                db.query(modelClass).filter_by(id=id).update(dict(form_data))
                db.commit()

                return HTTPException(200, 'Updated successfully')

            except IntegrityError:
                return HTTPException(400, 'Something went wrong')
            except Exception:
                return HTTPException(400, 'Internal server error')

        if not "delete" in ignorables:
            @self.delete("/delete/{id}")
            async def delete_one(id: int,  db: Session = ActiveSession):

                try:
                    record = db.get(modelClass, id)

                    if not record:
                        raise HTTPException(400, "Record was not found")

                    db.query(modelClass).filter_by(id=id).delete()
                    db.commit()

                    return HTTPException(200, 'Updated successfully')

                except IntegrityError:
                    return HTTPException(400, 'Something went wrong')
                except Exception:
                    return HTTPException(400, 'Internal server error')
