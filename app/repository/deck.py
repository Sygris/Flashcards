from .base import BaseRepository
from app.db.models.deck import Deck


class DeckRepository(BaseRepository):
    def create_deck(self, deck: Deck):
        pass
