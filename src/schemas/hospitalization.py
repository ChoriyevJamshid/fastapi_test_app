from datetime import date
from pydantic import BaseModel


class HospitalizationBase(BaseModel):
    admission_date: date
    discharge_date: date | None = None

class HospitalizationSchema(HospitalizationBase):
    doctor_id: int
    patient_id: int

class CreateHospSchema(HospitalizationBase):
    doctor_id: int

class UpdateHospSchema(HospitalizationBase):
    doctor_id: int