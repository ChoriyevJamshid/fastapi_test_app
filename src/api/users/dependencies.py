from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import connector
from src.models import User
from src.schemas.users import UserUpdateSchema

from src.api.auth.dependencies import get_current_active_user, get_admin_user


async def update_user(
        user_update: UserUpdateSchema,
        user: Annotated[User, Depends(get_current_active_user)],
        admin: Annotated[User, Depends(get_admin_user)],
        session: Annotated[AsyncSession, Depends(connector.generate_session)]
):
    for key, value in user_update.model_dump().items():
        setattr(user, key, value)
    await session.commit()
    return user



async def delete_user(
        user: Annotated[User, Depends(get_current_active_user)],
        session: Annotated[AsyncSession, Depends(connector.generate_session)],
        admin: Annotated[User, Depends(get_admin_user)],
):
    await session.delete(user)
    await session.commit()


