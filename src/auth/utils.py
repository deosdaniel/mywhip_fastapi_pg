from datetime import timedelta, datetime, timezone
import jwt
import uuid
import logging
import bcrypt
from src.config import Config

ACCESS_TOKEN_EXPIRY = 900


def gen_pwd_hash(password: str) -> str:
    pwd_encoded = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(pwd_encoded, salt=salt)
    return hashed_pwd.decode("utf-8")


def verify_pwd(plain_pwd: str, hashed_pwd: str) -> bool:
    plain_pwd_encoded = plain_pwd.encode("utf-8")
    hashed_pwd_encoded = hashed_pwd.encode("utf-8")
    return bcrypt.checkpw(plain_pwd_encoded, hashed_pwd_encoded)


def create_access_token(user_uid: str, expiry: timedelta = None):
    payload = {
        "sub": user_uid,
        "exp": datetime.now(timezone.utc)
        + (expiry if expiry else timedelta(seconds=ACCESS_TOKEN_EXPIRY)),
        "jti": str(uuid.uuid4()),
    }
    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )
    return token


def decode_token(token: str) -> dict:

    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.error(f"JWT decoding failed: {e}")
        return None
