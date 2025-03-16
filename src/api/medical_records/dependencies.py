from fastapi import Depends, HTTPException, status, Form
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.dependencies import get_admin_user
from src.db import connector
from src.models import MedicalRecords, User
from src.schemas.medical_records import CreateMedicalRecord, UpdateMedicalRecord


async def get_medical_record(
        patient_id: int,
        session: Annotated[AsyncSession, Depends(connector.generate_session)]
) -> MedicalRecords:
    stmt = (
        select(
            MedicalRecords
        ).where(
            MedicalRecords.patient_id == patient_id
        )
    )
    result = await session.execute(stmt)
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Medical Record not found"
        )
    return record


async def create_medical_record(
        patient_id: int,
        new_medical_record_data: Annotated[Form, Depends(CreateMedicalRecord)],
        session: Annotated[AsyncSession, Depends(connector.generate_session)]
) -> MedicalRecords:
    new_medical_record = MedicalRecords(
        **new_medical_record_data.model_dump(),
        patient_id=patient_id,
    )
    session.add(new_medical_record)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Medical record already exists",
        )
    return new_medical_record


async def update_medical_record(
        medical_record: Annotated[MedicalRecords, Depends(get_medical_record)],
        update_medical_record_data: Annotated[Form, Depends(UpdateMedicalRecord)],
        session: Annotated[AsyncSession, Depends(connector.generate_session)]
) -> MedicalRecords:
    for key, value in update_medical_record_data.model_dump().items():
        setattr(medical_record, key, value)

    await session.commit()
    return medical_record


async def delete_medical_record(
        medical_record: Annotated[MedicalRecords, Depends(get_medical_record)],
        session: Annotated[AsyncSession, Depends(connector.generate_session)],
        admin: Annotated[User, Depends(get_admin_user)],
) -> None:
       await session.delete(medical_record)



