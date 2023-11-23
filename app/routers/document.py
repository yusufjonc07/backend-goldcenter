from fastapi import HTTPException, APIRouter, Depends, UploadFile
from typing import List, Optional
from app.schemas.user import NewUser
from app.utils.fileUtil import save_file, validate_file
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.document import *
from app.functions.document import *

document_router = APIRouter(tags=['Document Endpoint'])

@document_router.get("/documents", description="This router returns list of the documents using pagination")
async def get_documents_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):   
    if not usr.userRole in ['any_role']:
        return get_all_documents(search, page, limit, usr, db)  
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")  

@document_router.post("/document/create", description="This router is able to add new document")
async def create_new_document(
    fileName: UploadFile,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        try:

            if db.query(Document).filter_by(fileName=fileName.filename).first():
                raise HTTPException(400, "Bu nomli hujjat mavjud")

            await validate_file(fileName, ['document'], 3)

            new_document = Document(
                fileName=fileName.filename,
                createdAt=func.now(),
            )

            db.add(new_document)
            db.commit()

            await save_file(fileName, fileName.filename, 'documents')

            raise HTTPException(200, "Ma`lumotlar saqlandi!")
        except IntegrityError as e:
            raise HTTPException(400, e.args)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@document_router.post("/document/create_list", description="This router is able to add new document")
async def create_new_documents(
    fileNames: List[UploadFile],
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:

        for fileName in fileNames:

            try:

                if not db.query(Document).filter_by(fileName=fileName.filename).first():

                    await validate_file(fileName, ['document'], 3)

                    new_document = Document(
                        fileName=fileName.filename,
                        createdAt=func.now(),
                    )

                    db.add(new_document)
                    db.commit()

                    await save_file(fileName, fileName.filename, 'documents')

                   
            except IntegrityError as e:
                raise HTTPException(400, e.args)
        raise HTTPException(200, "Ma`lumotlar saqlandi!")
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
