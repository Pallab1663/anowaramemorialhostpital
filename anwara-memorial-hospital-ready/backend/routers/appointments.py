import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from lib.db import db
from models.appointment import Appointment, AppointmentCreate
from routers.data import DOCTORS
router = APIRouter()
@router.post("/appointments", response_model=Appointment, status_code=201)
async def create_appointment(input: AppointmentCreate):
    if not any(d.id == input.doctor_id for d in DOCTORS): raise HTTPException(400, "Invalid doctor")
    now=datetime.now(timezone.utc); document={**input.model_dump(),"id":str(uuid.uuid4()),"status":"pending","scheduled_date":None,"scheduled_time":None,"admin_note":None,"created_at":now,"updated_at":now}
    await db.appointments.insert_one(document); return Appointment(**document)
