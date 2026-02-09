from app.db.database import Base, engine

# Models that need to be created need to be import
from app.db.models.user import User
from app.db.models.deck import Deck


def create_tables():
    Base.metadata.create_all(bind=engine)
