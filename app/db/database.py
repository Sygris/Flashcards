from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import config

# Creates the connection to the database
engine = create_engine(config.db_url, echo=True)

# Creates the Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


# Returns a Session from the factory
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
