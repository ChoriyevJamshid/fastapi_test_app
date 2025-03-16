from typing import Annotated
from fastapi import (
    APIRouter,
    status,
    Depends,
)

from src.models import MedicalRecords
from src.schemas.medical_records import MedicalRecordSchema
from src.api.medical_records.dependencies import (
    get_medical_record,
    create_medical_record,
    update_medical_record,
    delete_medical_record
)

router = APIRouter(prefix="/medical_records", tags=["Medical Records"])


@router.get("/{patient_id}", response_model=MedicalRecordSchema)
async def get_medical_records(
        medical_record: Annotated[MedicalRecords, Depends(get_medical_record)],
):
    return medical_record


@router.post(
    "/{patient_id}",
    response_model=MedicalRecordSchema,
    status_code=status.HTTP_201_CREATED
)
async def add_medical_records(
        created_medical_record: Annotated[MedicalRecords, Depends(create_medical_record)],
):
    return created_medical_record


@router.put(
    "/{patient_id}",
    response_model=MedicalRecordSchema,
    status_code=status.HTTP_200_OK
)
async def update_medical_records(
        medical_record: Annotated[MedicalRecords, Depends(update_medical_record)],
):
    return medical_record


@router.delete(
    "/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(delete_medical_record)],
)
async def delete_medical_records():
    pass
