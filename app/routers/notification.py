from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException
from config import ALGORITHM, SECRET_KEY
from databases.main import ActiveSession
from app.utils.wsmanager import *
from app.models.user import *
from app.schemas.user import NewUser
from app.schemas.notification import MessageSchema
from security.auth import jwt

notification_router = APIRouter()


# @notification_router.get("/send_to_public")
# async def send_to_public(title: str, description: str, db: Session = ActiveSession):

#     message = MessageSchema(
#         title=title,
#         body=description,
#         imgurl="https://api2.f9.crud.uz/images/galery/niso-logo.png"
#     )

#     return await manager.send_user(message, 'plant_admin', db)


@notification_router.websocket("/connection")
async def websocket_endpoint(
    token: str,
    websocket: WebSocket,
    db: Session = ActiveSession
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")

    user: User = db.query(User).filter_by(
        username=username, disabled=False).first()

    await manager.connect(websocket, user)

    try:

        if user:
            for ntf in user.notifications:
                await manager.send_personal_json(ntf.body, (websocket, user))

            db.query(Notification).filter_by(user_id=user.id).delete()
            db.commit()

        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
