from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.user import User
from app.db.schemas.user import UserOut, UserUpdateIn
from app.core.security.dependencies import get_current_user
from app.service.user import UserService

# Cretes the router
router = APIRouter()


# User Profile
@router.get("/profile", response_model=UserOut, status_code=200)
def profile(current_user: User = Depends(get_current_user)):
    return current_user


# Update User details (email, password and/or nickname)
@router.patch("/update", response_model=UserOut, status_code=200)
def update_user(
    updates: UserUpdateIn,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    return UserService(session).update_user(current_user, updates)
