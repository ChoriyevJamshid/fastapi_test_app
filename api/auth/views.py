from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Form,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import db, User
from api.auth.schemas import (
    Token,
    UserRegisterSchema,
    UserSchema, UserLoginSchema
)

from api.auth import utils as auth_utils
from api.auth import dependencies as auth_dependencies

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register/", response_model=UserSchema)
async def auth_register(
        new_data: Annotated[Form, Depends(UserRegisterSchema)],
        session: AsyncSession = Depends(db.generate_session)
):
    stmt = select(User).where(User.email == new_data.email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
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


@router.post("/login/", response_model=Token)
async def auth_login(
        user: UserLoginSchema = Depends(auth_dependencies.validate_user_login)
):
    access_token = auth_dependencies.create_access_token(user)
    return Token(access_token=access_token, token_type="Bearer")


@router.post("/logout/")
async def auth_logout():
    pass


@router.get("/me/")
async def auth_me(user: User = Depends(auth_dependencies.get_current_active_user)):
    return {
        "email": user.email,
        "role": user.role,
        "active": user.active,
    }
