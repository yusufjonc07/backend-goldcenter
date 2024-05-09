from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.category import *
from app.functions.category import *
from app.schemas.category import *

category_router = APIRouter(tags=['Category Endpoint'])


@category_router.get("/categories", description="This router returns list of the categorys using pagination")
async def get_categorys_list(
    search: Optional[str] = "",
    type: Optional[CategoryTypes] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_categorys(search, type, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@category_router.post("/category/create", description="This router is able to add new category")
async def create_new_category(
    form_data: NewCategory,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_category(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@category_router.put("/category/{id}/update", description="This router is able to update category")
async def update_one_category(
    id: int,
    form_data: UpdateCategory,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_category(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
