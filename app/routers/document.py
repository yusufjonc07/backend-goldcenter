from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.document import *
from app.functions.document import *
from app.schemas.document import *

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
    form_data: NewDocument,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_document(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")

@document_router.put("/document/{id}/update", description="This router is able to update document")
async def update_one_document(
    id: int,
    form_data: UpdateDocument,
    db:Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_document(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
