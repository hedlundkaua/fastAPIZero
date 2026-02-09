from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESSS_TOKEN_EXPIRE_MINUTES = 30
pwd_contex = PasswordHash.recommended()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESSS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_contex.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_contex.verify(plain_password, hashed_password)
