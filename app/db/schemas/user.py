from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nickname: str | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    nickname: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    id: int
    email: EmailStr | None = None
    password: str | None = None
    nickname: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# TODO: Save refresh_token in HTTP-Only cookies
class UserWithToken(BaseModel):
    token: str
    refresh_token: str
