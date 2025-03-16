from datetime import date

from pydantic import BaseModel

from src.models.patients import GenderEnum, StatusEnum

class PatientBase(BaseModel):
    full_name: str
    birth_date: date
    gender: GenderEnum
    contact_info: str
    status: StatusEnum

class CreatePatientSchema(PatientBase):
    pass

class UpdatePatientSchema(PatientBase):
    pass

class PatientSchema(PatientBase):
    id: int