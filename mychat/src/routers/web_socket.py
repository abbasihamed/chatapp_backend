from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException

from mychat.src.db.database import mongo_client
from mychat.src.controller.web_socket_controller import WebSocketManager

from mychat.src.crud import rooms_crud

router = APIRouter(tags=['chat'])

socket_manager = WebSocketManager()


@router.websocket('/email={email}')
async def chat_websocket(email: str, websocket: WebSocket):
    await socket_manager.connect(websocket=websocket, email=email)
    await socket_manager.send_rooms(email)
    try:
        while True:
            receive_message = await websocket.receive_text()
            await socket_manager.send_message(receive_message)
    except WebSocketDisconnect:
        print('sfddsd')


@router.get('/get-old-message/sender={sender}/receiver={receiver}')
async def get_old_message(sender: str, receiver: str):
    chat = rooms_crud.find_room(
        value=[{'members': [sender, receiver]}, {'members': [receiver, sender]}], mode='$or')
    if not chat:
        raise HTTPException(detail='No Exist', status_code=404)
    return rooms_crud.roomEntity(chat)

# {"message.id": id}, {'message.$': 1}


@router.get('/find-delete={id}/{email}')
async def find_delelte(id: str, email: str):
    chat = mongo_client.telegram.rooms.find_one_and_update(
        {"message.id": '63ab1cc6e3322155dd8941a9'}, {'$pull': {'message.$.viewers': email}})
    return None


@router.get('/find={email}')
async def find(email: str):
    return rooms_crud.find_rooms(email)
