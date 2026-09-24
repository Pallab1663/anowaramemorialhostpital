import asyncio, os
import uuid
from datetime import datetime, timezone
from lib.auth import hash_password
from lib.db import client, db, ensure_indexes
async def seed():
    email=os.environ.get("ADMIN_EMAIL","admin@anwarahospital.com"); password=os.environ.get("ADMIN_PASSWORD")
    if not password: raise RuntimeError("Set ADMIN_PASSWORD before seeding the admin account")
    if not await db.admin_users.find_one({"email":email}):
        await db.admin_users.insert_one({"id":str(uuid.uuid4()),"email":email,"name":"Anwara Hospital Admin","role":"super_admin","password_hash":hash_password(password),"active":True,"created_at":datetime.now(timezone.utc)})
        print(f"Seeded {email}")
    await ensure_indexes(); client.close()
if __name__=="__main__": asyncio.run(seed())
