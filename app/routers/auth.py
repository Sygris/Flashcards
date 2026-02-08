from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security.dependencies import get_current_user
from app.db.database import get_db
from app.db.schemas.user import UserCreate, UserLogin, UserRead
from app.db.schemas.auth import UserWithToken, RefreshRequest
from app.service.user import UserService
from app.service.auth import AuthService

router = APIRouter()


@router.post("/login", status_code=200, response_model=UserWithToken)
def login(loginDetails: UserLogin, session: Session = Depends(get_db)):
    try:
        return AuthService(session).login(loginDetails)
    except Exception as Error:
        print(Error)
        raise Error


@router.post("/signup", status_code=201, response_model=UserRead)
def signup(signupDetails: UserCreate, session: Session = Depends(get_db)):
    try:
        return UserService(session).create_user(signupDetails)
    except Exception as Error:
        print(Error)
        raise Error


@router.post("/logout", status_code=200)
def logout(
    current_user: UserRead = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    AuthService(session).logout(current_user.id)
    return {"status": "Logged out successfully"}


@router.post("/refresh", status_code=200)
def refresh_token(request: RefreshRequest, session: Session = Depends(get_db)):
    new_access_token = AuthService(session).refresh_access_token(request.refresh_token)
    return {"new_access_token": new_access_token, "token_type": "bearer"}
