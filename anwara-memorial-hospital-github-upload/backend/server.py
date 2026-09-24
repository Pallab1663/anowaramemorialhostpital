import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from lib.auth import hash_password
from lib.db import db, ensure_indexes
from routers.admin import router as admin_router
from routers.appointments import router as appointments_router
from routers.auth import router as auth_router
from routers.public import router as public_router

logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = BASE_DIR.parent / "frontend" / "dist"


async def ensure_seed_admin() -> None:
    """Create the first admin from Render environment variables when needed."""
    email = os.environ.get("ADMIN_EMAIL", "").strip().lower()
    password = os.environ.get("ADMIN_PASSWORD", "")
    name = os.environ.get("ADMIN_NAME", "Anwara Hospital Admin").strip()

    if not email or not password:
        logger.warning("ADMIN_EMAIL/ADMIN_PASSWORD are not set; no admin seed was attempted.")
        return

    existing = await db.admin_users.find_one({"email": email})
    if existing:
        return

    import uuid
    from datetime import datetime, timezone

    await db.admin_users.insert_one(
        {
            "id": str(uuid.uuid4()),
            "email": email,
            "name": name,
            "role": "super_admin",
            "password_hash": hash_password(password),
            "active": True,
            "created_at": datetime.now(timezone.utc),
        }
    )
    logger.info("Seeded initial admin account %s", email)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_indexes()
    await ensure_seed_admin()
    yield


api_router = APIRouter()


@api_router.get("/")
async def api_root():
    return {"message": "Anwara Memorial Hospital API", "service": "hospital-website"}


api_router.include_router(public_router)
api_router.include_router(appointments_router)
api_router.include_router(auth_router)
api_router.include_router(admin_router)


app = FastAPI(
    title="Anwara Memorial Hospital API",
    version="1.0.0",
    lifespan=lifespan,
)

allowed_origins = [origin.strip() for origin in os.environ.get("CORS_ORIGINS", "").split(",") if origin.strip()]
if not allowed_origins:
    allowed_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "anwara-memorial-hospital"}

# In production the FastAPI service serves the built React app too, so the
# browser only needs one origin and the admin cookie remains same-origin.
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")


@app.get("/{path:path}", include_in_schema=False)
async def frontend(path: str):
    if path == "api" or path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API route not found")
    if not FRONTEND_DIST.exists():
        return {"message": "Frontend build not found. Run `npm run build` in frontend/."}

    requested = FRONTEND_DIST / path
    if path and requested.is_file():
        return FileResponse(requested)

    index = FRONTEND_DIST / "index.html"
    return FileResponse(index)
