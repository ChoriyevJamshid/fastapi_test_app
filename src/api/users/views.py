from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status
)

from src.models import User
from src.schemas.users import UserSchema
from src.api.users.dependencies import update_user, delete_user

router = APIRouter(prefix="/users", tags=["users"])


@router.put("/{user_id}/", response_model=UserSchema)
async def update_user(
        user: Annotated[User, Depends(update_user)]
):
    return user


@router.delete(
    "/{user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(delete_user)],
)
async def delete_user():
    pass
