from pydantic import BaseModel, ConfigDict, EmailStr


class UserIn(BaseModel):
    email: EmailStr
    password: str
    nickname: str | None = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    nickname: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdateIn(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    nickname: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str
