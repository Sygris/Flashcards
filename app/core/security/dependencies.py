from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security.auth_handler import AuthHandler, oauth2_scheme
from app.db.database import get_db
from app.db.models.user import User
from app.service.user import UserService


# Returns the data of the user doing the request
def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db),
) -> User:
    # Saves HTTPException in a variable to avoid duplicated code
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Authentication Credentials",
    )

    payload = AuthHandler.decode_token(token)

    if not payload or not payload.get("sub"):
        raise auth_exception

    try:
        user = UserService(session).get_user_by_id(payload["sub"])
        return user
    except Exception:
        raise auth_exception
