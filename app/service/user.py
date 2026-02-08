from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repository.user import UserRepository
from app.db.schemas.user import (
    UserRead,
    UserCreate,
)
from app.core.security.hash_helper import HashHelper


class UserService:
    def __init__(self, session: Session):
        self._user_repository = UserRepository(session)

    def create_user(self, user_details: UserCreate) -> UserRead:
        if self._user_repository.get_user_by_email(user_details.email):
            raise HTTPException(status_code=400, detail="Please Login")

        hashed_password = HashHelper.hash_password(user_details.password)
        user_details.password = hashed_password

        user = self._user_repository.create_user(user_details)
        return UserRead.model_validate(user)

    def get_user_by_id(self, user_id: int):
        user = self._user_repository.get_user_by_id(user_id)

        if user:
            return user

        raise HTTPException(status_code=400, detail="User is not available")
