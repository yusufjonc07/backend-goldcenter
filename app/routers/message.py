import uuid
from fastapi import Body, File, HTTPException, APIRouter, Depends, UploadFile
from typing import Optional
from app.routers.employee import CONTENT_TYPE_LOOKUP_TABLE
from app.schemas.user import NewUser
from app.utils.handler import integrityHandler
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


@message_router.post("/message/create")
async def create_new_message(
    context: Optional[str] = Body(None),
    fileName: Optional[UploadFile] = File(None),
    forRole: ChatTypes = Body(...),
    replyId: Optional[int] = Body(None),
    branchId: Optional[int] = Body(...),
    db: Session = ActiveSession,
    usr: User = Depends(get_current_active_user)
):
    if not usr.userRole in ['any_role']:
        try:

            if fileName is None and context is None:
                raise HTTPException(400, 'Xabar tarkibidi nimadir bo`lishi kerak')

            if fileName is not None:
                if not fileName.content_type in CONTENT_TYPE_LOOKUP_TABLE:
                    raise HTTPException(400, "Fayl formati noto`g`ri!")

                file_contents = await fileName.read()
                _fileName = f"{uuid.uuid4()}__{fileName.filename}"

                if len(file_contents) > 3000000:
                    raise HTTPException(400, "Fayl kattaligi maksimal 3 MB!")

                with open(f"assets/clientAgreements/{_fileName}", "wb") as f:
                    f.write(file_contents)
            else:
                _fileName = None

            new_message = Message(
                fileName=_fileName,
                context=context,
                forRole=forRole,
                replyId=replyId,
                userId=usr.id,
                branchId=branchId,
            )

            db.add(new_message)
            db.commit()
            db.refresh(new_message)

            await manager.send_user(new_message, usr, db)

            raise HTTPException(200, "Ma`lumotlar saqlandi!")
        except IntegrityError as e:
            raise integrityHandler(e)
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
