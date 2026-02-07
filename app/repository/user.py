from sqlalchemy import select
from .base import BaseRepository

from app.db.models.user import User
from app.db.schemas.user import UserCreate


class UserRepo(BaseRepository):
    def create_user(self, user_data: UserCreate):
        new_user = User(**user_data.model_dump(exclude_none=True))

        try:
            self.session.add(new_user)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

        self.session.refresh(new_user)
        return new_user

    def user_exist_by_email(self, email: str) -> bool:
        stmt = select(User).where(User.email == email)
        user = self.session.execute(stmt).scalar_one_or_none()

        return user is not None

    def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        user = self.session.execute(stmt).scalar_one_or_none()

        return user

    def get_user_by_id(self, user_id: int) -> User | None:
        user = self.session.get(User, user_id)

        return user
