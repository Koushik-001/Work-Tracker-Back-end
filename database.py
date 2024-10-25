from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)

db = client.task_manager
tasks_collection = db["tasks"]
