from typing import Annotated

from fastapi import Depends, HTTPException, status, Form
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Hospitalization
from src.schemas.hospitalization import CreateHospSchema, UpdateHospSchema
from src.db import connector


async def get_hospitalization(
        patient_id: int,
        session: Annotated[AsyncSession, Depends(connector.generate_session)]
):
    stmt = select(Hospitalization).where(Hospitalization.patient_id == patient_id)
    result = await session.execute(stmt)
    hospitalization = result.scalar_one_or_none()
    if not hospitalization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospitalization not found"
        )
    return hospitalization


async def create_hospitalization(
        patient_id: int,
        new_hospitalization: Annotated[Form, Depends(CreateHospSchema)],
        session: Annotated[AsyncSession, Depends(connector.generate_session)],
):
    hosp = Hospitalization(**new_hospitalization.model_dump())
    hosp.patient_id = patient_id
    session.add(hosp)

    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return hosp



async def update_hospitalization(
        hospitalization: Annotated[Hospitalization, Depends(get_hospitalization)],
        session: Annotated[AsyncSession, Depends(connector.generate_session)],
        update_hospitalization: Annotated[Form, Depends(UpdateHospSchema)]
):
    for key, value in update_hospitalization.model_dump(exclude_unset=True).items():
        setattr(hospitalization, key, value)
    await session.commit()
    return hospitalization


async def delete_hospitalization(
        hospitalization: Annotated[Hospitalization, Depends(get_hospitalization)],
        session: Annotated[AsyncSession, Depends(connector.generate_session)]
):
    await session.delete(hospitalization)



