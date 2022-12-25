from mychat.src.db.database import mongo_client


def roomEntity(item):
    return {
        'id': str(item['_id']),
        'room_name': item['room_name'],
        'members': item['members'],
        'messages': item['message']
    }

def roomList(item):
    return {
        'id': str(item['_id']),
        'room_name': item['room_name'],
        # 'members': item['members'],
        'messages': item['message'].pop()
    }


def roomsEntity(entity):
    return [roomList(room) for room in entity]


def get_room(room_name: str):
    return mongo_client.telegram.rooms.find_one({'room_name': room_name})


def find_rooms(email):
    return roomsEntity(mongo_client.telegram.rooms.find({'members': {'$in': [email]}}).sort('datetime', -1))


def create_room(room_data: dict):
    mongo_client.telegram.rooms.insert_one(room_data)


def find_room(value, mode: str):
    return mongo_client.telegram.rooms.find_one({mode: value})


def find_room_update(room_name: str, value: dict, mode: str = '$set'):
    return mongo_client.telegram.rooms.find_one_and_update(
        {'room_name': room_name}, {mode: value})
