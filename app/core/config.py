from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    app_name: str = "Flashcards"
    debug: bool = False
    db_user: str = ""
    db_password: str = ""
    db_name: str = "flashcards"

    @property
    def db_url(self):
        return f"postgresql://{self.db_user}:{self.db_password}@localhost:5432/{self.db_name}"


config = Config()
