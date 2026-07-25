from pymongo import MongoClient
from config import MONGO_URI, DATABASE

client = MongoClient(MONGO_URI)

db = client[DATABASE]

employees = db.employees