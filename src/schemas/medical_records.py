from datetime import datetime

from pydantic import BaseModel


class MedicalRecordBase(BaseModel):
    created_at: datetime
    diagnosis: str
    treatment: str

class MedicalRecordSchema(MedicalRecordBase):
    patient_id: int
    doctor_id: int

class CreateMedicalRecord(MedicalRecordBase):
    doctor_id: int

class UpdateMedicalRecord(MedicalRecordBase):
    doctor_id: int



