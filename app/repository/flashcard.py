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
        stmt = (
            select(Flashcard)
            .join(Deck, Flashcard.deck_id == Deck.id)
            .where(Deck.id == deck_id, Deck.owner_id == user_id)
            .group_by(Flashcard.id)
        )
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

    def does_flashcard_exist(
        self, deck_id: int, user_id: int, question: str, answer: str
    ) -> bool:
        stmt = (
            select(Flashcard)
            .join(Deck, Flashcard.deck_id == Deck.id)
            .where(
                Deck.id == deck_id,
                Deck.owner_id == user_id,
                Flashcard.question == question,
                Flashcard.answer == answer,
            )
        )

        flashcard = self.session.scalars(stmt).first()
        return flashcard is not None

    def update_flashcard(self, flashcard: Flashcard, updates: dict):
        for name, value in updates.items():
            setattr(flashcard, name, value)

        try:
            self.session.commit()
            self.session.refresh(flashcard)
        except Exception:
            self.session.rollback()
            raise

        return flashcard

    def delete_flashcard(self, flashcard: Flashcard):
        try:
            self.session.delete(flashcard)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
