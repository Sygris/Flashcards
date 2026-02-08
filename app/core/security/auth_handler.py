import jwt
import secrets
from jwt import PyJWTError
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
from app.core.config import config


class AuthHandler:
    oauth2 = OAuth2PasswordBearer("/auth/login")

    @staticmethod
    def create_token(data: dict) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=config.access_token_expire_minutes
        )

        payload = data.copy()
        payload["exp"] = expire

        token = jwt.encode(payload, config.jwt_secret, config.jwt_algorithm)

        return token

    @staticmethod
    def decode_token(token: str) -> dict | None:
        try:
            payload = jwt.decode(
                token, config.jwt_secret, algorithms=[config.jwt_algorithm]
            )
            return payload
        except PyJWTError:
            print("Unable to decode the token")
            return None

    @staticmethod
    def create_refresh_token() -> str:
        return secrets.token_urlsafe(64)
