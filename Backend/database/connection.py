import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017"
)

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "task_manager"
)

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000,
)

database = client[DATABASE_NAME]
tasks_collection = database["tasks"]


def check_database_connection() -> bool:
    """Check whether MongoDB is reachable."""
    try:
        client.admin.command("ping")
        return True
    except PyMongoError:
        return False


def close_database_connection() -> None:
    """Close the MongoDB client."""
    client.close()
