from typing import Annotated
from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from app.core.security.auth_handler import AuthHandler
from app.db.database import get_db
from app.db.models.user import User
from app.service.user import UserService

AUTH_PREFIX = "Bearer "


# Returns the data of the user doing the request
def get_current_user(
    session: Session = Depends(get_db),
    authorization: Annotated[str | None, Header()] = None,  # Takes the
) -> User:
    # Saves HTTPException in a variable to avoid duplicated code
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Authentication Credentials",
    )

    # If the request does not contain the authorization header raise the HTTPException
    if not authorization:
        raise auth_exception

    # if the header authorization does not start with "Bearer " raise the HTTPException
    if not authorization.startswith(AUTH_PREFIX):
        raise auth_exception

    # Cuts out the prefix (just reads the token itself)
    payload = AuthHandler.decode_token(authorization[len(AUTH_PREFIX) :])

    # If the payload was decoded and contains the key "sub" return the user
    if payload and payload["sub"]:
        try:
            # Get the user using the id from the payload
            user = UserService(session).get_user_by_id(payload["sub"])
            return user
        except Exception as Error:
            raise Error

    raise auth_exception
