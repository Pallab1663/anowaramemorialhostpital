import os
import hashlib
from fastapi import APIRouter, HTTPException, Request, Response
from lib.auth import SESSION_COOKIE, create_session, get_current_admin, public_user, verify_password
from lib.db import db
from models.auth import AdminLogin, AdminLoginResponse, AdminUser
router=APIRouter()
@router.post("/auth/login", response_model=AdminLoginResponse)
async def login(input: AdminLogin,response: Response):
    admin=await db.admin_users.find_one({"email":str(input.email).lower().strip(),"active":True})
    if not admin or not verify_password(input.password,admin.get("password_hash","")): raise HTTPException(401,"Incorrect email or password")
    token=await create_session(admin["id"]); secure=os.environ.get("COOKIE_SECURE","false").lower()=="true"
    response.set_cookie(SESSION_COOKIE,token,httponly=True,max_age=60*60*24*int(os.environ.get("SESSION_DAYS", "7")),samesite="lax",secure=secure,path="/")
    return AdminLoginResponse(user=public_user(admin))
@router.get("/auth/me",response_model=AdminUser)
async def me(request:Request): _,user=await get_current_admin(request); return user
@router.post("/auth/logout",status_code=204)
async def logout(request:Request,response:Response):
    raw=request.cookies.get(SESSION_COOKIE)
    if raw: await db.sessions.delete_one({"token_hash":hashlib.sha256(raw.encode()).hexdigest()})
    response.delete_cookie(SESSION_COOKIE,path="/")
