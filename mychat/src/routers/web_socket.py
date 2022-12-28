import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException

from mychat.src.controller.web_socket_controller import WebSocketManager

from mychat.src.crud import rooms_crud
from mychat.src.core.enums import ChatEnum

router = APIRouter(tags=['chat'])

socket_manager = WebSocketManager()


@router.websocket('/email={email}')
async def chat_websocket(email: str, websocket: WebSocket):
    await socket_manager.connect(websocket=websocket, email=email)
    await socket_manager.send_rooms(email)
    try:
        while True:
            receive_message = await websocket.receive_text()
            r = json.loads(receive_message)
            if r['request_mode'] == ChatEnum.message.name:
                await socket_manager.send_message(receive_message)
            if r['request_mode'] == ChatEnum.delete.name:
                await socket_manager.delete_message(receive_message)

    except WebSocketDisconnect:
        print('sfddsd')


@router.get('/get-old-message/sender={sender}/receiver={receiver}')
async def get_old_message(sender: str, receiver: str):
    chat = rooms_crud.find_room(
        value=[{'members': [sender, receiver]}, {'members': [receiver, sender]}], mode='$or')
    if not chat:
        raise HTTPException(detail='No Exist', status_code=404)
    return rooms_crud.roomEntity(chat)


@router.get('/find={email}')
async def find(email: str):
    return rooms_crud.find_rooms(email)
