from pydantic import BaseModel


# TODO: Save refresh_token in HTTP-Only cookies
class UserWithToken(BaseModel):
    token: str
    refresh_token: str


class RefreshRequest(BaseModel):
    refresh_token: str
