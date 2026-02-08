from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.user import UserRepository
from app.core.security.auth_handler import AuthHandler
from app.core.security.hash_helper import HashHelper
from app.db.models.user import User
from app.db.schemas.user import UserLogin
from app.db.schemas.auth import UserWithToken


class AuthService:
    def __init__(self, session: Session):
        self._user_repository = UserRepository(session)

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

    def refresh_access_token(self, refresh_token: str) -> str:
        user = self._user_repository.get_user_by_refresh_token(refresh_token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        new_payload = {"sub": str(user.id), "role": user.role.value}
        new_access_token = AuthHandler.create_token(new_payload)
        return new_access_token

    def save_refresh_token(self, user: User, refresh_token: str) -> User:
        return self._user_repository.update_user(user, {"refresh_token": refresh_token})

    def remove_refresh_token(self, user: User) -> User:
        return self._user_repository.update_user(user, {"refresh_token": None})
