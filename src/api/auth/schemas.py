from pydantic import BaseModel, EmailStr, ConfigDict
from src.core.models import RoleEnum

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


# class UserSchema(BaseModel):
#     model_config = ConfigDict(strict=True)
#     username: EmailStr
#     password: bytes
#     active: bool = True


class UserBaseSchema(BaseModel):
    email: EmailStr
    role: RoleEnum
    active: bool = True


class UserRegisterSchema(UserBaseSchema):
    password: str


class UserLoginSchema(BaseModel):
    username: EmailStr
    password: str
    role: RoleEnum
    active: bool = True

class UserSchema(UserBaseSchema):
    pass


