import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from lib.db import ensure_indexes
from routers.admin import router as admin_router
from routers.appointments import router as appointments_router
from routers.auth import router as auth_router
from routers.public import router as public_router
logger=logging.getLogger(__name__)
@asynccontextmanager
async def lifespan(app:FastAPI):
    await ensure_indexes(); yield
api_router=APIRouter()
@api_router.get("/")
async def root(): return {"message":"Anwara Memorial Hospital API","service":"hospital-website"}
api_router.include_router(public_router); api_router.include_router(appointments_router); api_router.include_router(auth_router); api_router.include_router(admin_router)
app=FastAPI(title="Anwara Memorial Hospital API",version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(api_router,prefix="/api")
