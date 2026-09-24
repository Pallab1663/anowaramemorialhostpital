import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from lib.auth import hash_password, require_roles
from lib.db import db
from models.appointment import Appointment, AppointmentStatus, AppointmentUpdate
from models.auth import AdminUser, AdminUserCreate
router=APIRouter()
def _appointment(d): return Appointment(**{k:v for k,v in d.items() if k!="_id"})
@router.get("/admin/appointments",response_model=list[Appointment])
async def list_appointments(status:AppointmentStatus|None=Query(None),doctor_id:str|None=Query(None),_:tuple[dict,AdminUser]=Depends(require_roles("super_admin","appointment_manager","doctor_assistant"))):
    f={};
    if status:f["status"]=status
    if doctor_id:f["doctor_id"]=doctor_id
    docs=await db.appointments.find(f).sort("created_at",-1).to_list(1000); return [_appointment(d) for d in docs]
@router.patch("/admin/appointments/{appointment_id}",response_model=Appointment)
async def update_appointment(appointment_id:str,input:AppointmentUpdate,_:tuple[dict,AdminUser]=Depends(require_roles("super_admin","appointment_manager","doctor_assistant"))):
    updates=input.model_dump(exclude_unset=True)
    if not updates: raise HTTPException(400,"No appointment changes supplied")
    updates["updated_at"]=datetime.now(timezone.utc); result=await db.appointments.update_one({"id":appointment_id},{"$set":updates})
    if not result.matched_count: raise HTTPException(404,"Appointment not found")
    return _appointment(await db.appointments.find_one({"id":appointment_id}))
@router.get("/admin/users",response_model=list[AdminUser])
async def list_admins(_:tuple[dict,AdminUser]=Depends(require_roles("super_admin"))):
    docs=await db.admin_users.find().sort("created_at",-1).to_list(100); return [AdminUser(**{k:v for k,v in d.items() if k not in {"_id","password_hash"}}) for d in docs]
@router.post("/admin/users",response_model=AdminUser)
async def create_admin(input:AdminUserCreate,_:tuple[dict,AdminUser]=Depends(require_roles("super_admin"))):
    email=str(input.email).lower().strip()
    if await db.admin_users.find_one({"email":email}): raise HTTPException(409,"An admin with this email already exists")
    d={"id":str(uuid.uuid4()),"email":email,"name":input.name.strip(),"role":input.role,"password_hash":hash_password(input.password),"active":True,"created_at":datetime.now(timezone.utc)}; await db.admin_users.insert_one(d); return AdminUser(**{k:v for k,v in d.items() if k!="password_hash"})
