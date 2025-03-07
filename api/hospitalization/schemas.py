from datetime import date

from pydantic import BaseModel


class HospitalizationBase(BaseModel):
    admission_date: date
    discharge_date: date | None = None


class CreateHospSchema(HospitalizationBase):
    doctor_id: int

class UpdateHospSchema(HospitalizationBase):
    doctor_id: int
