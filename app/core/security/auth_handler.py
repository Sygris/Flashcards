import jwt
import secrets
from jwt import PyJWTError
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
from app.core.config import config


# Class to handle the JWT creation and reading
class AuthHandler:
    oauth2 = OAuth2PasswordBearer("/auth/login")

    # Creates the token and returns it
    @staticmethod
    def create_token(data: dict) -> str:
        # Access Token expiration (now + minutes set in .env)
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=config.access_token_expire_minutes
        )

        # Copies the data sent to create_token (e.g: sub and role)
        payload = data.copy()
        # Adds the expiration to the payload
        payload["exp"] = expire

        # Encodes the payload using the secret and algorithm set in .env/Config class
        token = jwt.encode(payload, config.jwt_secret, config.jwt_algorithm)

        return token

    # Decodes the access token to retrieve the payload
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

    # Used to create the refresh token
    @staticmethod
    def create_refresh_token() -> str:
        return secrets.token_urlsafe(64)
