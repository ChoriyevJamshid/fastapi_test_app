from pydantic import BaseModel, EmailStr

from core.models import RoleEnum


class UserBase(BaseModel):
    email: EmailStr
    role: RoleEnum
    active: bool


class UserSchema(BaseModel):
    id: int

class UserUpdateSchema(UserBase):
    pass



