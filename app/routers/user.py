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
@router.get("/profile")
def profile(current_user: UserOut = Depends(get_current_user)):
    return {"Hello": current_user.nickname}


# Update User details (email, password and/or nickname)
@router.patch("/update")
def update_user(
    updates: UserUpdateIn,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> UserOut:
    updated_user = UserService(session).update_user(
        current_user, updates
    )  # Gets the User with the updated data
    return UserOut.model_validate(
        updated_user
    )  # Returns the user using the schema to validate the output
