from fastapi import HTTPException, APIRouter, Depends, Query
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.branch import *
from app.functions.branch import *
from app.schemas.branch import *

branch_router = APIRouter(tags=['Filial Endpoint'])


@branch_router.get("/branchs", description="This router returns list of the branchs using pagination")
async def get_branchs_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_branchs(search, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@branch_router.get("/branch_one", description="This router returns list of the branchs using pagination")
async def get_branch_one(
    id: int,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return db.get(Branch, id)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@branch_router.post("/branch/create", description="This router is able to add new branch")
async def create_new_branch(
    form_data: NewBranch,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return create_branch(form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@branch_router.put("/branch/{id}/update", description="This router is able to update branch")
async def update_one_branch(
    id: int,
    form_data: UpdateBranch,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_branch(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@branch_router.delete("/delete_practices")
async def delete_practices_all(
    confirmation: Optional[str] = Query(...,
                                        description="Tasdiqlayman deb yozing"),
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    """
    !!!DIQQAT!!!
    Ehtiyot bo'ling barcha ma'lumotlar tozalanadi!
    Va ularni orqaga qaytarib bo'lmaydi!!!
    """

    if confirmation != "Tasdiqlayman":
        raise HTTPException(status_code=400, detail="Tasdiqlanmadi!")

    if not usr.userRole in ['any_role']:
        return delete_practices(usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
