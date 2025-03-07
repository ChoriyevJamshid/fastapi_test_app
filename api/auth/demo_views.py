import jwt
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    Form,
)
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from api.auth.schemas import UserSchema
from api.auth import utils as auth_utils


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


router = APIRouter(prefix="", tags=["jwt"])

# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

john = UserSchema(
    username="john@example.com",
    password=auth_utils.hash_password("qwerty")
)

sam = UserSchema(
    username="sam@example.com",
    password=auth_utils.hash_password("secret")
)

users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam
}


def validate_auth_user_login(
        username: EmailStr = Form(),
        password: str = Form(),
):
    unauthed_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )

    if not (user := users_db.get(username)):
        raise unauthed_exp

    if not auth_utils.validate_password(
            password=password,
            hashed_password=user.password
    ):
        raise unauthed_exp

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not active",
        )

    return user


def get_current_token_payload(
        # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        token: str = Depends(oauth2_scheme),
):
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(token)
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials, {e = }",
        )
    return payload


def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload),
):
    username: str = payload.get("sub")
    if (user := users_db.get(username)):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid, (user no found)",
    )


def get_current_active_auth_user(
        user: UserSchema = Depends(get_current_auth_user),
):
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user

TOKEN_TYPE = "type"
ACCESS_TOKEN = "access"
REFRESH_TOKEN = "refresh"

def create_jwt(token_type: str, token_data: dict) -> str:
    jwt_payload = {TOKEN_TYPE: token_type}
    jwt_payload.update(token_data)
    return auth_utils.encode_jwt(jwt_payload)


def create_access_token(
        user: UserSchema,
) -> str:
    jwt_payload = {
        "sub": user.username,
    }
    return create_jwt(ACCESS_TOKEN, jwt_payload)

def create_refresh_toke(
        user: UserSchema,
) -> str:
    jwt_payload = {"sub": user.username,}
    return create_jwt(REFRESH_TOKEN, jwt_payload)


@router.post("/login", response_model=TokenInfo)
def auth_user_jwt_login(
        user: UserSchema = Depends(validate_auth_user_login),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_toke(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.get("/me")
def auth_jwt_me(
        user: UserSchema = Depends(get_current_active_auth_user),
):
    return {
        "email": user.username,
    }
