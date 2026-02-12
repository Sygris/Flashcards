from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.deck import Deck
from app.db.models.user import User
from app.db.schemas.deck import DeckIn
from app.repository.deck import DeckRepository


class DeckService:
    def __init__(self, session: Session) -> None:
        self._deck_repository = DeckRepository(session)

    def create_deck(self, deck_data: DeckIn, user: User) -> Deck:
        if self._deck_repository.get_user_deck_by_title(deck_data.title, user.id):
            raise HTTPException(status_code=409, detail="Deck title already exists")

        deck = Deck(**deck_data.model_dump(exclude_none=True))
        deck.owner_id = user.id

        return self._deck_repository.create_deck(deck)

    def get_deck_by_id(self, deck_id: int, user: User) -> Deck:
        deck = self._deck_repository.get_users_deck_by_id(deck_id, user.id)

        if deck:
            return deck

        raise HTTPException(status_code=404, detail="Deck not found")

    def get_all_decks(self, user: User) -> list[Deck]:
        decks = self._deck_repository.list_decks_by_owner(user.id)

        if decks:
            return decks

        raise HTTPException(status_code=404, detail="No deck found")

    def update_deck(self, deck_id: int, user: User, updates: DeckIn) -> Deck:
        deck = self.get_deck_by_id(deck_id, user)

        if deck is None:
            raise HTTPException(status_code=404, detail="Deck not found")

        updated_deck = self._deck_repository.update_deck(
            deck, updates.model_dump(exclude_none=True)
        )
        return updated_deck

    def delete_deck(self, deck_id: int, user: User):
        deck = self.get_deck_by_id(deck_id, user)

        if deck is None:
            raise HTTPException(status_code=404, detail="Deck not found")

        return self._deck_repository.delete_deck(deck)
