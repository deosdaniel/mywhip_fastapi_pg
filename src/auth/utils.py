from passlib.context import CryptContext
from passlib.handlers.bcrypt import bcrypt

pwd_context = CryptContext(
    schemes=[bcrypt]
)

def generate_pwd_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_pwd(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)