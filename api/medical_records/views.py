from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Form,
    status
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import db
from core.models import Patient, MedicalRecords, User, RoleEnum
from api.auth import dependencies as auth_dependencies
from api.medical_records.schemas import (
    CreateMedicalRecord,
    UpdateMedicalRecord,
)

router = APIRouter(prefix="/medical_records", tags=["Medical Records"])


@router.get("/{patient_id}")
async def get_medical_records(
        patient_id: int,
        session: AsyncSession = Depends(db.generate_session)
):
    stmt = select(MedicalRecords).where(MedicalRecords.patient_id == patient_id)
    result = await session.execute(stmt)
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical Record not found")
    return record


@router.post("/{patient_id}")
async def add_medical_records(
        patient_id: int,
        new_mr_data: Annotated[Form, Depends(CreateMedicalRecord)],
        session: AsyncSession = Depends(db.generate_session),
):
    # checking patient
    patient = await session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    new_mr = MedicalRecords(
        **new_mr_data.model_dump(),
        patient_id=patient_id,
    )
    session.add(new_mr)
    await session.commit()
    return {
        "message": "Create medical records",
        "id": new_mr.id
    }


@router.put("/{patient_id}")
async def update_medical_records(
        patient_id: int,
        update_mr_data: Annotated[Form, Depends(UpdateMedicalRecord)],
        session: AsyncSession = Depends(db.generate_session),
):
    patient = await session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    stmt = select(MedicalRecords).where(MedicalRecords.patient_id == patient_id)
    result = await session.execute(stmt)
    mr = result.scalars().first()
    if not mr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    for key, value in update_mr_data.model_dump().items():
        setattr(mr, key, value)
    await session.commit()
    return {
        "message": "Update medical records",
    }


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medical_records(
        patient_id: int,
        session: Annotated[AsyncSession, Depends(db.generate_session)],
        user: Annotated[User, Depends(auth_dependencies.get_current_active_user)]
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    if not user.role == RoleEnum.doctor:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    patient = await session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    stmt = select(MedicalRecords).where(MedicalRecords.patient_id == patient_id)
    result = await session.execute(stmt)
    mr = result.scalars().first()
    if not mr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    await session.delete(mr)
    await session.commit()
