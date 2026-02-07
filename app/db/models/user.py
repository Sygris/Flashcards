from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)
    nickname: Mapped[str | None] = mapped_column(String, nullable=True)

    refresh_token: Mapped[str | None] = mapped_column(String, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
