from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field
AppointmentStatus = Literal["pending", "confirmed", "rescheduled", "cancelled"]
class AppointmentCreate(BaseModel):
    patient_name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=7, max_length=30)
    email: str | None = Field(default=None, max_length=160)
    doctor_id: str = Field(min_length=1)
    preferred_date: str = Field(min_length=8, max_length=10)
    preferred_time: str = Field(min_length=2, max_length=40)
    message: str | None = Field(default=None, max_length=1000)
class Appointment(AppointmentCreate):
    id: str; status: AppointmentStatus; scheduled_date: str | None = None; scheduled_time: str | None = None; admin_note: str | None = None; created_at: datetime; updated_at: datetime
class AppointmentUpdate(BaseModel):
    status: AppointmentStatus | None = None
    scheduled_date: str | None = Field(default=None, max_length=10)
    scheduled_time: str | None = Field(default=None, max_length=40)
    admin_note: str | None = Field(default=None, max_length=1000)
