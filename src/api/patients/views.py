from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    status,
)

from src.models import Patient
from src.schemas.patients import PatientSchema
from src.api.patients import dependencies as patient_dep


router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("/{patient_id}", response_model=PatientSchema)
async def get_patient(
        patient: Annotated[Patient, Depends(patient_dep.get_patient_by_id)]
):
    return patient


@router.post(
    "/",
    response_model=PatientSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_patient(
        new_patient: Annotated[Patient, Depends(patient_dep.create_patient)]
):
    return new_patient


@router.put(
    "/{patient_id}",
    response_model=PatientSchema,
    status_code=status.HTTP_200_OK
)
async def update_patient(
        updated_patient: Annotated[Patient, Depends(patient_dep.update_patient)]
):
    return updated_patient



@router.delete(
    "/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(patient_dep.delete_patient)]
)
async def delete_patient(
) -> None:
    return
