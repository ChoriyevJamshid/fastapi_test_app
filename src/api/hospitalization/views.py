from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from src.models import Hospitalization
from src.schemas.hospitalization import HospitalizationSchema
from src.api.hospitalization.dependencies import (
    create_hospitalization,
    update_hospitalization,
    delete_hospitalization
)

router = APIRouter(prefix="/hospitalization", tags=["Hospitalization"])


@router.post(
    "/{patient_id}",
    response_model=HospitalizationSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_patient_hospitalization(
        hospitalization: Annotated[Hospitalization, Depends(create_hospitalization)],
):
    return hospitalization


@router.patch(
    "/{patient_id}",
    response_model=HospitalizationSchema,
    status_code=status.HTTP_200_OK
)
async def update_patient_hospitalization(
        updated_hospitalization: Annotated[Hospitalization, Depends(update_hospitalization)]
):
    return updated_hospitalization


@router.delete(
    "/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(delete_hospitalization)]
)
async def delete_patient_hospitalization():
    pass
