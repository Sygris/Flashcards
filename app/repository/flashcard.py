from sqlalchemy import select
from app.db.models.deck import Deck
from app.db.models.flashcard import Flashcard
from .base import BaseRepository


class FlashcardRepository(BaseRepository):
    def create_flashcard(self, flashcard: Flashcard):
        try:
            self.session.add(flashcard)
            self.session.commit()
            self.session.refresh(flashcard)
        except Exception:
            self.session.rollback()
            raise

        return flashcard

    def list_flashcards(self, deck_id: int, user_id: int):
        stmt = select(Flashcard).where(Flashcard.deck_id == deck_id)
        flashcards = self.session.scalars(stmt).all()

        return flashcards

    def get_flashcard(self, flashcard_id: int, deck_id: int, user_id: int):
        stmt = (
            select(Flashcard)
            .join(Deck, Flashcard.deck_id == Deck.id)
            .where(
                Flashcard.id == flashcard_id,
                Deck.id == deck_id,
                Deck.owner_id == user_id,
            )
        )
        flashcard = self.session.scalars(stmt).one_or_none()

        return flashcard
