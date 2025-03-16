from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from core import User
from core.db_connector import db
from api.auth import dependencies as auth_dependencies
from api.users.schemas import (
    UserSchema,
    UserUpdateSchema,
)
from core.models import RoleEnum

router = APIRouter(prefix="/users", tags=["users"])


@router.put("/{user_id}/", response_model=UserSchema)
async def update_user(
        edited_user_id: int,
        user_update: UserUpdateSchema,
        session: Annotated[AsyncSession, Depends(db.generate_session)],
        user: Annotated[User, Depends(auth_dependencies.get_current_active_user)],
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    if not user.role == RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    edited_user = await session.get(User, edited_user_id)
    if not edited_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_update.model_dump().items():
        setattr(edited_user, key, value)
    await session.commit()


@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        deleted_user_id: int,
        session: Annotated[AsyncSession, Depends(db.generate_session)],
        user: Annotated[User, Depends(auth_dependencies.get_current_active_user)]
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    if not user.role == RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    deleted_user = await session.get(User, deleted_user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(deleted_user)
    await session.commit()
