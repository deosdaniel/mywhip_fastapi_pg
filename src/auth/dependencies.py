from typing import Annotated
from fastapi import Depends, HTTPException, status
from src.users.schemas import UserSchema
from src.users.service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from fastapi.security import OAuth2PasswordBearer

from src.auth.utils import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> UserSchema:

    token_data = decode_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid or expired"
        )
    check_user = UserService()
    user = await check_user.get_user_by_uid(token_data["sub"], session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user
