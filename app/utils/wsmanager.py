from fastapi import WebSocket, WebSocketException, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.models.message import Message
from app.models.user import User
from app.models.notification import Notification


class ConnectionManager:

    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket, user):
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

    async def send_personal_json(self, message: dict, connection):
        websocket, user = connection
        try:
            await websocket.send_json({
                "title": message['title'],
                "body": message['body'],
                "imgUrl": message['imgurl'],
            })

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

    async def send_user(self, message: Message, usr: User, db: Session):

        users = db.query(User.id).filter_by(userRole=message.forRole).all()


        for employee in users:
            sent = False
            for connection in self.active_connections:
                websocket, user = connection
                try:
                    
                    if user.id == employee.id:
                        try:
                            await websocket.send_json(message)
                        except Exception as e:
                            print(e)

                        sent = True

                except WebSocketDisconnect:
                    await self.disconnect(websocket)

            if sent == False:
                db.add(Notification(
                    title=message['title'],
                    body=message,
                    imgUrl=message['imgUrl'],
                    user_id=employee.id
                ))
                db.commit()

        return


manager = ConnectionManager()
