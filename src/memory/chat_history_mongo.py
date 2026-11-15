"""
MongoDB client configuration using Motor async driver.
"""

import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URL = (
    os.getenv("MONGODB_URL")
    or os.getenv("MONGO_URL")
    or os.getenv("MONGO_URI")
    or os.getenv("MONGODB_URI")
)

MONGODB_DB_NAME = (
    os.getenv("MONGODB_DB_NAME")
    or os.getenv("MONGO_DB_NAME")
    or os.getenv("DB_NAME")
    or "adaptive_rag"
)

if not MONGODB_URL:
    raise ValueError(
        "Missing MongoDB connection string! Set MONGODB_URL in your environment variables."
    )

client = AsyncIOMotorClient(MONGODB_URL)
db = client[MONGODB_DB_NAME]
