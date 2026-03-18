from sqlalchemy.orm import Session
from app.db.models.deck import Deck
from app.schemas.deck import DeckIn
from app.repository.deck import DeckRepository


class DeckService:
    def __init__(self, session: Session) -> None:
        self._deck_repository = DeckRepository(session)

    def create_deck(self, deck_data: DeckIn, user_id: int) -> Deck:
        if self._deck_repository.get_user_deck_by_title(deck_data.title, user_id):
            raise ValueError("Deck already exists")

        deck = Deck(**deck_data.model_dump(exclude_unset=True))
        deck.owner_id = user_id

        return self._deck_repository.create_deck(deck)

    def get_deck_by_id(self, deck_id: int, user_id: int) -> Deck:
        result = self._deck_repository.get_users_deck_by_id(deck_id, user_id)

        if result is None:
            raise LookupError("Deck not found")

        deck = result[0]
        deck.flashcard_count = result[1]

        return deck

    def get_all_decks(self, user_id: int) -> list[Deck]:
        results = self._deck_repository.list_decks_by_owner(user_id)

        decks = []
        for deck, count in results:
            deck.flashcard_count = count
            decks.append(deck)

        return list(decks)

    def update_deck(self, deck_id: int, user_id: int, updates: DeckIn) -> Deck:
        deck = self.get_deck_by_id(deck_id, user_id)

        if updates.title and self._deck_repository.get_user_deck_by_title(
            updates.title, user_id
        ):
            raise ValueError("Deck already exists")

        updated_deck = self._deck_repository.update_deck(
            deck, updates.model_dump(exclude_unset=True)
        )
        return updated_deck

    def delete_deck(self, deck_id: int, user_id: int):
        deck = self.get_deck_by_id(deck_id, user_id)
        return self._deck_repository.delete_deck(deck)
