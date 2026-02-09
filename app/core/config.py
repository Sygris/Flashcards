from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


# Basically a settings class where it centrailizes every "setting"
# It will load from .env
class Config(BaseSettings):
    app_name: str = "Flashcards"
    debug: bool = False
    db_user: str = ""
    db_password: str = ""
    db_name: str = "flashcards"

    jwt_secret: str = ""
    jwt_algorithm: str = ""
    access_token_expire_minutes: int = 30

    # It builds the postgresql connection string
    @property
    def db_url(self):
        return f"postgresql://{self.db_user}:{self.db_password}@localhost:5432/{self.db_name}"


config = Config()
