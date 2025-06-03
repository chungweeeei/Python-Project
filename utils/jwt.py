import jwt
import datetime 
from typing import Optional

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 2 * 60

def generate_access_token(email: str, expires_delta: Optional[datetime.timedelta] = None) -> str:

    now = datetime.datetime.now(datetime.timezone.utc)

    expire = now + expires_delta if expires_delta is not None else now + datetime.timedelta(minutes=60 * 24)

    encoded_jwt = jwt.encode({"sub": email, "exp": expire},
                             SECRET_KEY,
                             algorithm=ALGORITHM)

    return encoded_jwt

def decode_token(token: str) -> dict:

    try:
        payload = jwt.decode(token,
                             SECRET_KEY,
                             algorithms=ALGORITHM)
        return payload
    except Exception as err:
        raise err
