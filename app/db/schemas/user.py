from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nickname: str | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    nickname: str | None = None


class UserUpdate(BaseModel):
    id: int
    email: EmailStr | None = None
    password: str | None = None
    nickname: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserWithToken(BaseModel):
    token: str
