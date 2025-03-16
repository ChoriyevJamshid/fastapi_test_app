from pydantic import BaseModel, EmailStr
from src.models.users import RoleEnum


class UserBase(BaseModel):
    email: EmailStr
    role: RoleEnum
    active: bool = True


class UserRegisterSchema(UserBase):
    password: str


class UserLoginSchema(UserRegisterSchema):
    pass


class UserSchema(UserBase):
    pass


class UserUpdateSchema(UserBase):
    pass