from tokenize import Triple
from fastapi import WebSocket, WebSocketException, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.models.task import Message
from app.models.user import User
from app.models.notification import Notification


def get_clean_message_dict(record: Message):
    return {
        "id": record.id,
        "context": str(record.context),
        "fileName": str(record.fileName),
        "isViewed": record.isViewed,
        "userId": record.userId,
        "forRole": str(record.forRole),
        "branchId": record.branchId,
        "replyId": record.replyId,
        "createdAt": str(record.createdAt),
        "updated_at": str(record.updated_at),
        "employeeName": str(record.user.employee.fullname())
    }


class ConnectionManager:

    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket, user):
        await websocket.accept()
        self.active_connections.append((websocket, user))
        await websocket.send_text("Siz WebSocketga Ulandingiz!")

    async def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection[0] == websocket:
                self.active_connections.remove(connection)
                break

    async def send_personal_message(self, message: str, connection):
        websocket, user = connection
        try:
            await websocket.send_text(message)
        except WebSocketDisconnect:
            await self.disconnect(websocket)

    async def send_personal_json(self, message, connection):
        websocket, user = connection
        try:
            await websocket.send_json(get_clean_message_dict(message))

        except WebSocketDisconnect:
            await self.disconnect(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            websocket, user = connection
            try:
                await websocket.send_text(message)
            except WebSocketDisconnect:
                await self.disconnect(websocket)

    async def broadcast_json(self, message):
        for connection in self.active_connections:
            websocket, user = connection
            try:
                await websocket.send_json(message)
            except WebSocketDisconnect:
                await self.disconnect(websocket)

    async def send_user(self, notification, usr: User, db: Session):

        users = db.query(User.id).filter(
            User.userRole.in_(notification['roles']),
            User.id != usr.id, User.disabled == False
        ).all()

        for employee in users:
            sent = False
            for connection in self.active_connections:
                websocket, user = connection
                try:
                    if user.id == employee.id:
                        await websocket.send_json(notification)
                        sent = True
                except WebSocketDisconnect:
                    await self.disconnect(websocket)

            if sent == False:
                new_notification = Notification(
                    title=f"{usr.employee.firstname} {usr.employee.firstname}",
                    body=notification['text'],
                    imgUrl=notification['imgUrl'],
                    user_id=employee.id
                )
                db.add(new_notification)
                db.commit()

        return


manager = ConnectionManager()
