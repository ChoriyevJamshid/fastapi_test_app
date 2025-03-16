from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import db, User
from api.auth import utils as auth_utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(
        session: Annotated[AsyncSession, Depends(db.generate_session)],
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


async def validate_user_login(
        session: AsyncSession = Depends(db.generate_session),
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
