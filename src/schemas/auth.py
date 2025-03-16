from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    email: EmailStr | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
