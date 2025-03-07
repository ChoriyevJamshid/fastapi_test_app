from email.header import Header
from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Form,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core import db
from core.models import Patient, User, RoleEnum
from api.auth import dependencies as auth_dependencies
from api.patients.schemas import (
    CreatePatientSchema,
    PatientSchema, UpdatePatientSchema,
)

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("/{patient_id}", response_model=PatientSchema)
async def get_patient(
        patient_id: int,
        session: Annotated[AsyncSession, Depends(db.generate_session)]
):

    patient = await session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("/", response_model=PatientSchema)
async def create_patient(
        new_patient: Annotated[Form, Depends(CreatePatientSchema)],
        session: AsyncSession = Depends(db.generate_session),
):
    # CreatePatientSchema.
    patient = Patient(
        full_name=new_patient.full_name,
        birth_date=new_patient.birth_date,
        gender=new_patient.gender,
        contact_info=new_patient.contact_info,
        status=new_patient.status,
    )
    session.add(patient)
    await session.commit()

    return patient


@router.put("/{patient_id}", response_model=PatientSchema)
async def update_patient(
        patient_id: int,
        update_patient: Annotated[Form, Depends(UpdatePatientSchema)],
        session: AsyncSession = Depends(db.generate_session),
):
    patient = await session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    for key, value in update_patient.model_dump().items():
        setattr(patient, key, value)
    await session.commit()
    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
        patient_id: int,
        session: Annotated[AsyncSession, Depends(db.generate_session)],
        user: Annotated[User, Depends(auth_dependencies.get_current_active_user)]
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    if not user.role == RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    patient = await session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    await session.delete(patient)
    await session.commit()
