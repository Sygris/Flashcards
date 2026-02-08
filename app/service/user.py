from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repository.user import UserRepository
from app.db.models.user import User
from app.db.schemas.user import (
    UserRead,
    UserCreate,
    UserLogin,
    UserUpdate,
    UserWithToken,
)
from app.core.security.hash_helper import HashHelper
from app.core.security.auth_handler import AuthHandler


class UserService:
    def __init__(self, session: Session):
        self._user_repository = UserRepository(session)

    def signup(self, user_details: UserCreate) -> UserRead:
        if self._user_repository.get_user_by_email(user_details.email):
            raise HTTPException(status_code=400, detail="Please Login")

        hashed_password = HashHelper.hash_password(user_details.password)
        user_details.password = hashed_password

        user = self._user_repository.create_user(user_details)
        return UserRead.model_validate(user)

    def login(self, login_details: UserLogin) -> UserWithToken:
        user = self._user_repository.get_user_by_email(login_details.email)

        if not user:
            raise HTTPException(status_code=400, detail="Please create an Account")

        if HashHelper.verify_password(login_details.password, user.password):
            payload = {"sub": str(user.id), "role": user.role.value}
            access_token = AuthHandler.create_token(payload)
            refresh_token = AuthHandler.create_refresh_token()

            self.save_refresh_token(user, refresh_token)

            # TODO: Save refresh_token in HTTP-Only cookies
            if access_token and refresh_token:
                return UserWithToken(token=access_token, refresh_token=refresh_token)

            raise HTTPException(status_code=500, detail="Unable to process request")

        raise HTTPException(status_code=400, detail="Please check your Credentials")

    def logout(self, user_id: int):
        user = self._user_repository.get_user_by_id(user_id)

        if user:
            self.remove_refresh_token(user)

        return {"detail": "Logged out successfully"}

    def save_refresh_token(self, user: User, refresh_token: str) -> User:
        return self._user_repository.update_user(user, {"refresh_token": refresh_token})

    def remove_refresh_token(self, user: User) -> User:
        return self._user_repository.update_user(user, {"refresh_token": None})

    def get_user_by_id(self, user_id: int):
        user = self._user_repository.get_user_by_id(user_id)

        if user:
            return user

        raise HTTPException(status_code=400, detail="User is not available")
