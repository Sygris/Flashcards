from pydantic_settings import BaseSettings, SettingsConfigDict


# Basically a settings class where it centrailizes every "setting"
# It will load from .env
class Config(BaseSettings):
    app_name: str = "Flashcards"
    debug: bool = False
    db_user: str = ""
    db_password: str = ""
    db_port: str = ""
    db_name: str = "flashcards"

    jwt_secret: str = ""
    jwt_algorithm: str = ""
    access_token_expire_minutes: int = 30

    # It builds the postgresql connection string
    @property
    def db_url(self):
        return f"postgresql://{self.db_user}:{self.db_password}@localhost:{self.db_port}/{self.db_name}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Config()
