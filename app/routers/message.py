from fastapi import Body, File, HTTPException, APIRouter, Depends, UploadFile
from typing import Optional
from app.schemas.user import NewUser
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.message import *
from app.functions.message import *
from app.schemas.message import *
from app.utils.wsmanager import manager
from app.schemas.enums import messageTypeLabels

message_router = APIRouter(tags=['Message Endpoint'])


@message_router.get("/messages", description="This router returns list of the messages using pagination")
async def get_messages_list(
    search: Optional[str] = "",
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return get_all_messages(search, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@message_router.post("/message/create", description="This router is able to add new message")
async def create_new_message(
    text: Optional[str] = Body(None),
    mediaFile: UploadFile = File(...),
    type: MessageTypes = Body(...),
    forRole: ChatTypes = Body(...),
    replyId:  Optional[int] = Body(0),
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:

        form_data = NewMessage(
            context=text,
            type=type,
            forrole=forRole,
            replyid=replyId,
        )

        res = create_message(form_data, usr, db)
        if res:

            sendingMessage = {
                'imgUrl': f"https://ui-avatars.com/api/?name={usr.employee.firstname}+{usr.employee.lastname}&background=random",
                'title': f"{usr.employee.fullname()}dan yangi xabar",
                'forRole': res.forRole,
                'body': res.context,
            }



            await manager.send_user(sendingMessage, res.forRole, db)

            return res

    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@message_router.put("/message/{id}/update", description="This router is able to update message")
async def update_one_message(
    id: int,
    form_data: UpdateMessage,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        return update_message(id, form_data, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
