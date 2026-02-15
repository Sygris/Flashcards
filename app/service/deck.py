from sqlalchemy.orm import Session
from app.db.models.deck import Deck
from app.db.schemas.deck import DeckIn
from app.repository.deck import DeckRepository


class DeckService:
    def __init__(self, session: Session) -> None:
        self._deck_repository = DeckRepository(session)

    def create_deck(self, deck_data: DeckIn, user_id: int) -> Deck:
        if self._deck_repository.get_user_deck_by_title(deck_data.title, user_id):
            raise ValueError("Deck already exists")

        deck = Deck(**deck_data.model_dump(exclude_none=True))
        deck.owner_id = user_id

        return self._deck_repository.create_deck(deck)

    def get_deck_by_id(self, deck_id: int, user_id: int) -> Deck:
        deck = self._deck_repository.get_users_deck_by_id(deck_id, user_id)

        if deck is None:
            raise LookupError("Deck not found")

        return deck

    def get_all_decks(self, user_id: int) -> list[Deck]:
        decks = self._deck_repository.list_decks_by_owner(user_id)
        return list(decks)

    def update_deck(self, deck_id: int, user_id: int, updates: DeckIn) -> Deck:
        deck = self.get_deck_by_id(deck_id, user_id)

        if updates.title and self._deck_repository.get_user_deck_by_title(
            updates.title, user_id
        ):
            raise ValueError("Deck already exists")

        updated_deck = self._deck_repository.update_deck(
            deck, updates.model_dump(exclude_none=True)
        )
        return updated_deck

    def delete_deck(self, deck_id: int, user_id: int):
        deck = self.get_deck_by_id(deck_id, user_id)
        return self._deck_repository.delete_deck(deck)
