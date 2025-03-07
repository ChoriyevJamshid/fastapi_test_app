from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Form,
    Header,
)
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from core import db, Patient
from core.models import Hospitalization, User, RoleEnum
from api.auth import dependencies as auth_dependencies
from api.hospitalization.schemas import (
    CreateHospSchema,
    UpdateHospSchema,
)

router = APIRouter(prefix="/hospitalization", tags=["Hospitalization"])


@router.post("/{patient_id}")
async def create_patient_hospitalization(
        new_hospitalization: Annotated[Form, Depends(CreateHospSchema)],
        patient_id: int,
        session: Annotated[AsyncSession, Depends(db.generate_session)],
        headers=Header(),
):
    # Checking user is doctor
    print(headers)
    patient = await session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    hosp = Hospitalization(**new_hospitalization.model_dump())
    hosp.patient_id = patient_id
    session.add(hosp)
    await session.commit()

    return {"Hospitalization": "Added"}


@router.patch("/{patient_id}")
async def update_patient_hospitalization(
        patient_id: int,
        update_hosp: Annotated[Form, Depends(UpdateHospSchema)],
        session: AsyncSession = Depends(db.generate_session)
):
    stmt = select(Hospitalization).where(Hospitalization.patient_id == patient_id)
    result = await session.execute(stmt)
    hosp = result.scalar_one_or_none()
    if not hosp:
        raise HTTPException(status_code=404, detail="Hospitalization not found")
    for key, value in update_hosp.model_dump(exclude_unset=True).items():
        setattr(hosp, key, value)
    await session.commit()
    return {"Hospitalization": "Updated"}


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient_hospitalization(
        patient_id: int,
        session: Annotated[AsyncSession, Depends(db.generate_session)]
):

    stmt = select(Hospitalization).where(
        Hospitalization.patient_id == patient_id
    )
    result = await session.execute(stmt)
    hosp = result.scalar_one_or_none()
    if not hosp:
        raise HTTPException(status_code=404, detail="Hospitalization not found")
    await session.delete(hosp)
