from sqlalchemy import select
from .base import BaseRepository

from app.db.models.user import User


class UserRepository(BaseRepository):
    def create_user(self, user: User) -> User:
        try:
            self.session.add(user)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

        self.session.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        user = self.session.execute(stmt).scalar_one_or_none()

        return user

    def get_user_by_id(self, user_id: int) -> User | None:
        user = self.session.get(User, user_id)

        return user

    def get_user_by_refresh_token(self, refresh_token: str) -> User | None:
        stmt = select(User).where(User.refresh_token == refresh_token)
        user = self.session.execute(stmt).scalar_one_or_none()

        return user

    def update_user(self, user: User, updates: dict) -> User:
        for name, value in updates.items():
            setattr(user, name, value)

        try:
            self.session.commit()
            self.session.refresh(user)
        except Exception:
            self.session.rollback()
            raise

        return user
