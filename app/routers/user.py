from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.schemas.user import UserRead
from app.core.security.dependencies import get_current_user
from app.service.user import UserService

router = APIRouter()


@router.get("/profile")
def profile(current_user: UserRead = Depends(get_current_user)):
    return {"Hello": current_user.nickname}


@router.patch("/update")
def update_user(
    updates: dict,
    current_user: UserRead = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> UserRead:
    return current_user
