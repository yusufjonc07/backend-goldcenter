from datetime import date
import uuid
from fastapi import Body, File, HTTPException, APIRouter, Depends, UploadFile
from typing import Optional
from app.schemas.user import NewUser
from app.utils.fileUtil import save_file, validate_file
from app.utils.handler import integrityHandler
from security.auth import get_current_active_user
from databases.main import ActiveSession
from sqlalchemy.orm import joinedload, Session
from app.models.message import *
from app.functions.message import *
from app.schemas.message import *
from app.utils.wsmanager import manager
from app.schemas.enums import messageTypeLabels

message_router = APIRouter(tags=['Xabar Endpoint'])



@message_router.get("/messages")
async def get_messages_list(
    isOnlyUnread: Optional[bool] = False,
    search: Optional[str] = "",
    forRole: ChatTypes = 'headCleaner',
    page: int = 1,
    limit: int = 10,
    db: Session = ActiveSession,
    usr: NewUser = Depends(get_current_active_user)
):
    '''
    
    `{
        'accountant': 'Bugxalteriya',
        'headConstructor': 'Xo\'jalik bo\'limi',
        'headGuard': 'Xavfsizlik bo\'limi',
        'headCleaner': 'Tozalik bo\'limi'
    }`
    
    '''

    if not usr.userRole in ['any_role']:
        return get_all_messages(search, isOnlyUnread, page, limit, usr, db)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")


@message_router.post("/message/create")
async def create_new_message(
    context: Optional[str] = Body(None),
    fileName: Optional[UploadFile] = File(None),
    forRole: ChatTypes = Body(...),
    replyId: int = Body(0),
    branchId: Optional[int] = Body(...),
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        try:

            if fileName is None and context is None:
                raise HTTPException(400, 'Xabar tarkibidi nimadir bo`lishi kerak')

            if fileName:
                _fileName = await validate_file(fileName, ['document', 'image', 'audio', 'video'], 3)
            else:
                _fileName = None

            new_message = Message(
                fileName=_fileName,
                context=context,
                forRole=forRole,
                replyId=replyId if replyId > 0 else None,
                userId=usr.id,
                branchId=branchId,
            )

            db.add(new_message)
            db.commit()
            db.refresh(new_message)

            await save_file(fileName, _fileName, f"{new_message.forRole}/{date.year}/{date.month}/{date.day}")

            await manager.send_user(new_message, usr, db)

            raise HTTPException(200, "Ma`lumotlar saqlandi!")
        except IntegrityError as e:
            raise integrityHandler(e)
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")



# @message_router.put("/message/{id}/update", description="This router is able to update message")
# async def update_one_message(
#     id: int,
#     form_data: UpdateMessage,
#     db: Session = ActiveSession,
#     usr: NewUser = Depends(get_current_active_user)
# ):
#     if not usr.userRole in ['any_role']:
#         return update_message(id, form_data, usr, db)
#     else:
#         raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")
