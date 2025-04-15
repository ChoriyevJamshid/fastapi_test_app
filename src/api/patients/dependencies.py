from typing import Annotated

from fastapi import Depends, HTTPException, status, Form, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import connector
from src.models import Patient
from src.models import User

from src.schemas.patients import CreatePatientSchema, UpdatePatientSchema

from src.api.auth.dependencies import get_admin_user


async def get_patient_by_id(
        patient_id: int,
        session: Annotated[AsyncSession, Depends(connector.generate_session)]
) -> Patient:
    patient = await session.get(
        Patient, patient_id
    )
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return patient


async def get_patients(
        session: Annotated[AsyncSession, Depends(connector.generate_session)],
        page: Annotated[int, Query()] = 1,
        count: Annotated[int, Query(ge=20, le=100)] = 20,
) -> list:
    offset = (page - 1) * count
    stmt = select(Patient).offset(offset).limit(count)
    result = await session.execute(stmt)
    patients = result.scalars().all()
    return list(patients)


async def create_patient(
        new_patient: Annotated[Form, Depends(CreatePatientSchema)],
        session: Annotated[AsyncSession, Depends(connector.generate_session)],
) -> Patient:
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


async def update_patient(
        patient: Annotated[Patient, Depends(get_patient_by_id)],
        update_patient: Annotated[Form, Depends(UpdatePatientSchema)],
        session: Annotated[AsyncSession, Depends(connector.generate_session)],
):
    for key, value in update_patient.model_dump().items():
        setattr(patient, key, value)
    await session.commit()
    return patient


async def delete_patient(
        patient: Annotated[Patient, Depends(get_patient_by_id)],
        session: Annotated[AsyncSession, Depends(connector.generate_session)],
        admin: Annotated[User, Depends(get_admin_user)],
):
    await session.delete(patient)
    await session.commit()
