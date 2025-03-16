from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status
)
from src.models import User
from src.schemas.auth import (
    Token
)
from src.schemas.users import (
    UserLoginSchema,
    UserSchema
)
from src.api.auth import dependencies as auth_dependencies

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/register/",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def auth_register(
        created_user: Annotated[User, Depends(auth_dependencies.create_new_user)]
):
    return created_user


@router.post(
    "/login/",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def auth_login(
        user: UserLoginSchema = Depends(auth_dependencies.validate_user_login)
):
    access_token = auth_dependencies.create_access_token(user)
    return Token(access_token=access_token, token_type="Bearer")


@router.post("/logout/")
async def auth_logout():
    pass


@router.get(
    "/me/",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def auth_me(
        user: Annotated[User, Depends(auth_dependencies.get_current_active_user)]
) -> User:
    return user
