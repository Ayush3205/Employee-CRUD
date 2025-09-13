from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging

MONGO_URL = "mongodb+srv://ayushgupta23332_db_user:UpjVGHw90RDpRU13@employees.h8pymqt.mongodb.net/"
DATABASE_NAME = "assessment_db"
COLLECTION_NAME = "employees"

class MongoDB:
    client: AsyncIOMotorClient = None
    database = None
mongodb = MongoDB()

async def connect_to_mongo():
    """Create database connection"""
    try:
        mongodb.client = AsyncIOMotorClient(MONGO_URL)
        mongodb.database = mongodb.client[DATABASE_NAME]
        
        await mongodb.client.admin.command('ping')
        print("Successfully connected to MongoDB")
        
        await mongodb.database[COLLECTION_NAME].create_index("employee_id", unique=True)
        print("Created unique index on employee_id")
        
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection"""
    if mongodb.client:
        mongodb.client.close()
        print("Disconnected from MongoDB")

def get_database():
    """Get database instance"""
    return mongodb.database

def get_collection():
    """Get employees collection"""
    return mongodb.database[COLLECTION_NAME]