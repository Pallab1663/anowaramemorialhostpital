import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING, IndexModel

load_dotenv(Path(__file__).parent.parent / ".env")

mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
db_name = os.environ.get("DB_NAME", "anwara_hospital")
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]
logger = logging.getLogger(__name__)

INDEXES = {
    "status_checks": [IndexModel([("timestamp", DESCENDING)], name="timestamp_desc")],
    "appointments": [
        IndexModel([("id", ASCENDING)], name="appointment_id", unique=True),
        IndexModel([("status", ASCENDING), ("created_at", DESCENDING)], name="appointment_status_created"),
        IndexModel([("doctor_id", ASCENDING), ("preferred_date", ASCENDING)], name="appointment_doctor_date"),
    ],
    "admin_users": [IndexModel([("email", ASCENDING)], name="admin_email", unique=True)],
    "sessions": [IndexModel([("token_hash", ASCENDING)], name="session_token", unique=True), IndexModel([("expires_at", ASCENDING)], name="session_expiry")],
}

async def ensure_indexes() -> None:
    for collection, models in INDEXES.items():
        for model in models:
            try:
                await db[collection].create_indexes([model])
            except Exception as exc:
                logger.error("ensure_indexes(%s.%s): %s", collection, model.document["name"], exc)
