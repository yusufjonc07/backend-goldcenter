from tokenize import Triple
from typing import List
from fastapi import WebSocket, WebSocketException, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.user import User
from app.models.notification import Notification
from app.schemas.enums import NotificationTypes, UserRoles


def get_json(record: Notification):
    return {
        "id": record.id,
        "context": record.context,
        "type": record.type,
        "isViewed": record.isViewed,
        "task_id": record.task_id,
    }


class ConnectionManager:

    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket, user):
        await websocket.accept()
        self.active_connections.append((websocket, user))

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
            await websocket.send_json(get_json(message))

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

    async def send_user(
            self, context: str,
            for_roles: List[UserRoles],
            type: NotificationTypes,
            task_id: any,
            usr: User, db: Session):

        users = db.query(User.id).filter(
            User.userRole.in_(for_roles),
            User.disabled == False
        ).all()

        nots = []

        for user in users:
            new_notification = Notification(
                context=context,
                user_id=user.id,
                type=type,
                task_id=task_id,
            )
            db.add(new_notification)
            db.commit()
            db.refresh(new_notification)
            nots.append(new_notification)



        for not_one in nots:
       
            for connection in self.active_connections:
                websocket, user = connection

                try:
                    if user.id == not_one.user_id:
                        await websocket.send_json(get_json(not_one))
                        not_one.isSend = True
                except WebSocketDisconnect:
                    await self.disconnect(websocket)


        db.commit()

        return


manager = ConnectionManager()
