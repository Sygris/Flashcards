from typing import Annotated
from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from app.core.security.auth_handler import AuthHandler
from app.db.database import get_db
from app.db.schemas.user import UserRead
from app.service.user import UserService

AUTH_PREFIX = "Bearer "


def get_current_user(
    session: Session = Depends(get_db),
    authorization: Annotated[str | None, Header()] = None,
) -> UserRead:
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Authentication Credentials",
    )

    if not authorization:
        raise auth_exception

    if not authorization.startswith(AUTH_PREFIX):
        raise auth_exception

    # Cuts out the prefix (just reads the token itself)
    payload = AuthHandler.decode_token(authorization[len(AUTH_PREFIX) :])

    if payload and payload["sub"]:
        try:
            user = UserService(session).get_user_by_id(payload["sub"])
            print(payload)
            return UserRead(id=user.id, email=user.email, nickname=user.nickname)
        except Exception as Error:
            raise Error

    raise auth_exception
