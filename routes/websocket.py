from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
import models


templates = Jinja2Templates(directory="templates")

# router = APIRouter()

router = APIRouter(
    prefix="/websocket",
    tags=["websocket"],
    responses={
        404: {"description": "Not found Here"}
    }
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

active_connections = {}

@router.get("/")
def websocket(request: Request):
    return templates.TemplateResponse(request, "websocket.html")

# @router.websocket("/ws/{user_id}")
# async def websocket_endpoint(
#     websocket: WebSocket,
#     user_id: int
# ):

#     await websocket.accept()

#     while True:

#         data = await websocket.receive_text()

#         await websocket.send_text(
#             f"User {user_id}: {data}"
#         )

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    db: Session = Depends(get_db)
):

    await websocket.accept()
    active_connections[user_id] = websocket

    try:

        while True:

            data = await websocket.receive_json()

            receiver_id = data["receiver_id"]
            message_text = data["message"]
            message = models.Message(
                sender_id=user_id,
                receiver_id=receiver_id,
                message=message_text
            )

            db.add(message)
            db.commit()

            if receiver_id in active_connections:

                await active_connections[
                    receiver_id
                ].send_json({
                    "sender_id": user_id,
                    "message": message_text
                })

    except WebSocketDisconnect:

        if user_id in active_connections:
            del active_connections[user_id]
            
@router.get("/messages/{receiver_id}")
def get_messages(
    request: Request,
    receiver_id: int,
    db: Session = Depends(get_db)
):
  
    user_id = request.session.get("id")

    messages = (
        db.query(models.Message)
        .filter(
            (models.Message.sender_id == user_id) &(models.Message.receiver_id == receiver_id)|
            (models.Message.sender_id == receiver_id) &
            (models.Message.receiver_id == user_id)
        )
        .all()
    )

    return messages

# @router.websocket("/ws")
# async def websocket_endpoint(
#     websocket: WebSocket
# ):

#     await websocket.accept()

#     while True:

#         data = await websocket.receive_text()

#         await websocket.send_text(
#             f"Message Received: {data}"
#         )