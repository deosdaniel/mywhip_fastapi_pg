from passlib.context import CryptContext
from passlib.handlers.bcrypt import bcrypt
from datetime import timedelta, datetime
from src.config import Config
import jwt
import uuid
import logging


pwd_context = CryptContext(schemes=[bcrypt])

ACCESS_TOKEN_EXPIRY = 3600


def generate_pwd_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_pwd(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    # Create and fill all the needed payload
    payload = {}
    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload["jti"] = str(uuid.uuid4())  # jti - JWT Token Identifier
    payload["refresh"] = refresh
    # Create the token
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
        logging.exception(e)
        return None
