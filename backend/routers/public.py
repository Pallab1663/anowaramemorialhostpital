from fastapi import APIRouter
from models.hospital import HospitalProfile, Doctor, Service, GalleryImage
from routers.data import PROFILE, DOCTORS, SERVICES, GALLERY
router = APIRouter()
@router.get("/hospital", response_model=HospitalProfile)
async def hospital(): return PROFILE
@router.get("/doctors", response_model=list[Doctor])
async def doctors(): return DOCTORS
@router.get("/services", response_model=list[Service])
async def services(): return SERVICES
@router.get("/gallery", response_model=list[GalleryImage])
async def gallery(): return GALLERY
