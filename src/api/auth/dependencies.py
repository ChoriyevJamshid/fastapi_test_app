from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import connector
from src.models import User
from src.api.auth import utils as auth_utils
from src.models.users import RoleEnum
from src.schemas.users import UserRegisterSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(
        session: Annotated[AsyncSession, Depends(connector.generate_session)],
        token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = auth_utils.decode_jwt(token)
    except jwt.ExpiredSignatureError as e:
        raise credentials_exception
    except jwt.InvalidTokenError as e:
        raise credentials_exception

    user_id = payload.get("sub", 0)
    user = await session.get(User, int(user_id))

    if not user:
        raise credentials_exception
    return user


async def get_current_active_user(
        user: Annotated[User, Depends(get_current_user)]
):
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return user


async def get_admin_user(
        user: Annotated[User, Depends(get_current_active_user)]
):
    if not user.role == RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    return user


async def validate_user_login(
        session: AsyncSession = Depends(connector.generate_session),
        username: EmailStr = Form(),
        password: str = Form(),
):
    unauthed_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )

    stmt = select(User).where(User.email == username)
    result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()

    if user is None:
        raise unauthed_exp

    if not auth_utils.validate_password(
            password=password,
            hashed_password=user.password_hash,
    ):
        raise unauthed_exp

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not active",
        )
    return user


def create_access_token(user: User):
    payload = {
        "sub": str(user.id),
        "email": user.email,
    }
    return auth_utils.encode_jwt(payload=payload)


async def create_new_user(
        new_data: Annotated[Form, Depends(UserRegisterSchema)],
        session: Annotated[AsyncSession, Depends(connector.generate_session)],
        admin: Annotated[User, Depends(get_admin_user)],
):

    stmt = (
        select(User).where(User.email == new_data.email)
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    if not auth_utils.is_valid_password(new_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is incorrect"
        )

    new_user = User(
        email=new_data.email,
        role=new_data.role,
        active=new_data.active,
        password_hash=auth_utils.hash_password(new_data.password),
    )
    session.add(new_user)
    await session.commit()
    return new_user
