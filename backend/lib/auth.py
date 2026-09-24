import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Request
from lib.db import db
from models.auth import AdminUser

SESSION_COOKIE = "anwara_admin_session"
SESSION_DAYS = int(os.environ.get("SESSION_DAYS", "7"))


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 210_000)
    return f"pbkdf2_sha256$210000${salt.hex()}${digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, rounds, salt_hex, digest_hex = encoded.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), int(rounds))
        return hmac.compare_digest(digest.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


def public_user(document: dict) -> AdminUser:
    return AdminUser(**{k: v for k, v in document.items() if k not in {"_id", "password_hash"}})


async def create_session(admin_id: str) -> str:
    raw = secrets.token_urlsafe(48)
    token_hash = hashlib.sha256(raw.encode()).hexdigest()
    now = datetime.now(timezone.utc)
    await db.sessions.insert_one({"id": secrets.token_hex(16), "token_hash": token_hash, "admin_id": admin_id, "expires_at": now + timedelta(days=SESSION_DAYS)})
    return raw


async def get_current_admin(request: Request) -> tuple[dict, AdminUser]:
    raw = request.cookies.get(SESSION_COOKIE)
    if not raw:
        raise HTTPException(status_code=401, detail="Authentication required")
    token_hash = hashlib.sha256(raw.encode()).hexdigest()
    session = await db.sessions.find_one({"token_hash": token_hash, "expires_at": {"$gt": datetime.now(timezone.utc)}})
    if not session:
        raise HTTPException(status_code=401, detail="Session expired")
    admin = await db.admin_users.find_one({"id": session["admin_id"], "active": True})
    if not admin:
        raise HTTPException(status_code=401, detail="Admin account unavailable")
    return session, public_user(admin)


def require_roles(*roles: str):
    async def dependency(request: Request):
        session, user = await get_current_admin(request)
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return session, user
    return dependency
