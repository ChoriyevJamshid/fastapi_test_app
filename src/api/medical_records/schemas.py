from datetime import datetime

from pydantic import BaseModel


class MedicalRecordBase(BaseModel):
    created_at: datetime
    diagnosis: str
    treatment: str


class CreateMedicalRecord(MedicalRecordBase):
    doctor_id: int

class UpdateMedicalRecord(MedicalRecordBase):
    doctor_id: int


