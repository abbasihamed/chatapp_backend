import json
from bson.objectid import ObjectId
from datetime import datetime
from collections import defaultdict
from fastapi import WebSocket

from mychat.src.crud import rooms_crud


class WebSocketManager:
    def __init__(self) -> None:
        self.connections: dict = defaultdict(dict)

    async def connect(self, websocket: WebSocket, email: str):
        await websocket.accept()
        self.connections[email] = websocket
        print(f'CONNECTIONS : {self.connections[email]}')

    async def send_message(self, receive_message):
        data = json.loads(receive_message)
        room_name = data['room_name']
        room = rooms_crud.get_room(room_name=room_name)
        if not room:
            room_init_data = {
                'room_name': room_name,
                'members': [
                    data['sender'], data['receiver']
                ],
                'datetime': datetime.now(),
                'message': [
                    {
                        'id': str(ObjectId()),
                        'sender': data['sender'],
                        'receiver':data['receiver'],
                        'body':data['body'],
                        'viewers':[data['sender'], data['receiver']],
                        'datetime':datetime.now(),
                    }
                ]
            }
            rooms_crud.create_room(room_data=room_init_data)
            member_list = [data['sender'], data['receiver']]
            data['datetime'] = datetime.now()
            for item in member_list:
                if self.connections[item] == {}:
                    continue
                await self.connections[item].send_text(json.dumps(data, default=str))
                await self.connections[item].send_text(json.dumps(rooms_crud.find_rooms(item), default=str))
        else:
            rooms_crud.find_room_update(
                room_name, {'datetime': datetime.now()})
            member = rooms_crud.find_room_update(room_name=room_name, value={
                'message': {
                    'id': str(ObjectId()),
                    'sender': data['sender'],
                    'receiver': data['receiver'],
                    'body': data['body'],
                    'viewers': [data['sender'], data['receiver']],
                    'datetime': datetime.now(),
                }
            }, mode='$addToSet')
            member_list = member['members']
            data['datetime'] = datetime.now()
            for member in member_list:
                if self.connections[member] == {}:
                    continue
                await self.connections[member].send_text(json.dumps(data, default=str))
                await self.connections[member].send_text(json.dumps(rooms_crud.find_rooms(member), default=str))

    async def send_rooms(self, email):
        await self.connections[email].send_text(json.dumps(rooms_crud.find_rooms(email), default=str))
