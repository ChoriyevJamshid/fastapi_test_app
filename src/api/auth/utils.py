import re
import jwt
import bcrypt
from datetime import timedelta, datetime, timezone
from src.core.config import settings


def encode_jwt(
        payload: dict,
        secret_key: str = settings.secret_key,
        algorithm: str = settings.algorithm,
        expire_timedelta: timedelta | None = None,
        expire_minutes: int = settings.access_token_expire_minutes,
):

    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=secret_key,
        algorithm=algorithm,
    )
    return encoded_jwt


def decode_jwt(
        token: str | bytes,
        secret_key: str = settings.secret_key,
        algorithm: str = settings.algorithm,
):
    decoded_jwt = jwt.decode(
        jwt=token,
        key=secret_key,
        algorithms=[algorithm],
    )
    return decoded_jwt


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
        password: str,
        hashed_password: str,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode(),
    )


def is_valid_password(password):
    pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
    return bool(re.match(pattern, password))


