from typing import TYPE_CHECKING
from fastapi import Depends, HTTPException, status, Request


from src.auth.schemas import UserSchema
from src.auth.utils import decode_token
from src.auth.service import UserService

from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session

if TYPE_CHECKING:
    from src.auth.routes import user_service


async def get_current_user(
    request: Request, session: AsyncSession = Depends(get_session)
) -> UserSchema:

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    token = auth_header.split(" ")[1]
    token_data = decode_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid or expired"
        )
    user_service = UserService()
    user = await user_service.get_user_by_uid(token_data["sub"], session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user
