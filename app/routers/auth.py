from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security.dependencies import get_current_user
from app.db.database import get_db
from app.db.schemas.user import UserCreate, UserLogin, UserRead, UserWithToken
from app.service.user import UserService

router = APIRouter()


@router.post("/login", status_code=200, response_model=UserWithToken)
def login(loginDetails: UserLogin, session: Session = Depends(get_db)):
    try:
        return UserService(session).login(loginDetails)
    except Exception as Error:
        print(Error)
        raise Error


@router.post("/signup", status_code=201, response_model=UserRead)
def signup(signupDetails: UserCreate, session: Session = Depends(get_db)):
    try:
        return UserService(session).signup(signupDetails)
    except Exception as Error:
        print(Error)
        raise Error


@router.post("/logout", status_code=200)
def logout(
    current_user: UserRead = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    UserService(session).logout(current_user.id)
    return {"status": "Logged out successfully"}
