from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repository.user import UserRepository
from app.db.models.user import User
from app.db.schemas.user import (
    UserIn,
    UserUpdateIn,
)
from app.core.security.hash_helper import HashHelper


class UserService:
    def __init__(self, session: Session):
        self._user_repository = UserRepository(session)

    def create_user(self, user_details: UserIn) -> User:
        if self._user_repository.get_user_by_email(user_details.email):
            raise HTTPException(status_code=409, detail="Email already exists")

        hashed_password = HashHelper.hash_password(user_details.password)

        user = User(
            email=user_details.email,
            password=hashed_password,
            nickname=user_details.nickname,
        )

        user = self._user_repository.create_user(user)
        return user

    def update_user(self, user: User, updates: UserUpdateIn) -> User:
        update_data = updates.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password"] = HashHelper.hash_password(update_data["password"])

        if "email" in update_data:
            existing_user = self._user_repository.get_user_by_email(
                update_data["email"]
            )
            if existing_user and existing_user.id != user.id:
                raise HTTPException(status_code=409, detail="Email already in use")

        return self._user_repository.update_user(user, update_data)

    def get_user_by_id(self, user_id: int):
        user = self._user_repository.get_user_by_id(user_id)

        if user:
            return user

        raise HTTPException(status_code=404, detail="User not found")
