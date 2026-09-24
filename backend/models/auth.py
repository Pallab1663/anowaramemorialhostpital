from datetime import datetime
from typing import Literal
from pydantic import BaseModel, EmailStr, Field

AdminRole = Literal["super_admin", "appointment_manager", "doctor_assistant"]

class AdminUser(BaseModel):
    id: str
    email: EmailStr
    name: str
    role: AdminRole
    active: bool
    created_at: datetime

class AdminLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=200)

class AdminLoginResponse(BaseModel):
    user: AdminUser

class AdminUserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=8, max_length=200)
    role: AdminRole
