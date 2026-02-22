from typing import Sequence
from sqlalchemy import Alias, func, select

from app.db.models.deck import Deck
from app.db.models.flashcard import Flashcard
from .base import BaseRepository


class DeckRepository(BaseRepository):
    def create_deck(self, deck: Deck):
        try:
            self.session.add(deck)
            self.session.commit()
            self.session.refresh(deck)
        except Exception:
            self.session.rollback()
            raise

        return deck

    def get_users_deck_by_id(self, deck_id: int, user_id: int) -> Deck | None:
        stmt = (
            select(Deck, func.count(Flashcard.id).label("flashcard_count"))
            .outerjoin(Flashcard, Flashcard.deck_id == Deck.id)
            .where(Deck.id == deck_id, Deck.owner_id == user_id)
            .group_by(Deck.id)
        )

        deck = self.session.execute(stmt).scalar_one_or_none()

        return deck

    def list_decks_by_owner(self, user_id: int) -> Sequence[Deck]:
        stmt = (
            select(Deck)
            .outerjoin(Flashcard, Flashcard.deck_id == Deck.id)
            .where(Deck.owner_id == user_id)
            .group_by(Deck.id)
        )
        return self.session.execute(stmt).scalars().all()

    def get_user_deck_by_title(self, deck_title: str, user_id: int) -> Deck | None:
        stmt = (
            select(Deck)
            .outerjoin(Flashcard, Flashcard.deck_id == Deck.id)
            .where(Deck.title == deck_title, Deck.owner_id == user_id)
            .group_by(Deck.id)
        )
        deck = self.session.execute(stmt).scalar_one_or_none()

        return deck

    def update_deck(self, deck: Deck, updates: dict):
        for name, value in updates.items():
            setattr(deck, name, value)

        try:
            self.session.commit()
            self.session.refresh(deck)
        except Exception:
            self.session.rollback()
            raise

        return deck

    def delete_deck(self, deck: Deck):
        try:
            self.session.delete(deck)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
