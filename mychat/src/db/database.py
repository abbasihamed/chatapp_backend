from pymongo import MongoClient
from mychat.src.core.constants import MONGODB_URL

mongo_client = MongoClient(MONGODB_URL)
