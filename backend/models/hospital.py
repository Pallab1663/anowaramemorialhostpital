from pydantic import BaseModel
class HospitalProfile(BaseModel):
    name_bn: str; name_en: str; tagline_bn: str; tagline_en: str; established: str; founder_name_en: str; founder_name_bn: str; founder_bio_en: str; founder_bio_bn: str; founder_image_url: str; address_en: str; address_bn: str; phone_emergency: str; phone_alt: str; whatsapp: str; email: str
class Doctor(BaseModel):
    id: str; name_bn: str; name_en: str; degrees: str; designation_bn: str; designation_en: str; workplace_bn: str; workplace_en: str; specialty: str; image_url: str
class Service(BaseModel):
    id: str; title_bn: str; title_en: str; desc_bn: str; desc_en: str
class GalleryImage(BaseModel):
    id: str; image_url: str; alt: str; label: str
