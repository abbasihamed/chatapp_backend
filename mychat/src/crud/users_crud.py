from datetime import datetime
from pymongo import TEXT

from mychat.src.db.database import mongo_client


def userEntity(item):
    return {
        'id': str(item['_id']),
        'email': item['email']
    }


def usersEntity(entity):
    return [userEntity(user) for user in entity]


def get_otp_code(code: int):
    return mongo_client.telegram.otp.find_one({'otp_code': code})


def set_otp_code(code: int):
    mongo_client.telegram.otp.insert_one(
        {'otp_code': code, 'datetime': datetime.now(), 'is_valid': True})


def update_otp_code(code: int):
    return mongo_client.telegram.otp.find_one_and_update(
        {'otp_code': code},
        {'$set': {'is_valid': False}}
    )


def search_user(email: str):
    return usersEntity(mongo_client.telegram.users.find({'email': {'$regex': email}}))


def get_user(email: str):
    return mongo_client.telegram.users.find_one({'email': email})


def create_user(email: str):
    query = get_user(email=email)
    if not query:
        mongo_client.telegram.users.insert_one({'email': email})
        return userEntity(get_user(email=email))
    return userEntity(query)
