from app.db.models.flashcard import Flashcard
from app.repository.deck import DeckRepository
from app.repository.flashcard import FlashcardRepository
from app.db.schemas.flashcard import FlashcardInCreate, FlashcardInUpdate


class FlashcardService:
    def __init__(self, session):
        self._flashcard_repository = FlashcardRepository(session)
        self._deck_repository = DeckRepository(session)

    def create_flashcard(
        self, flashcard_data: FlashcardInCreate, deck_id: int, user_id: int
    ) -> Flashcard:
        deck = self._deck_repository.get_users_deck_by_id(deck_id, user_id)

        if deck is None:
            raise LookupError("Deck not found")

        flashcard = Flashcard(
            **flashcard_data.model_dump(exclude_unset=True), deck_id=deck_id
        )

        return self._flashcard_repository.create_flashcard(flashcard)

    def list_flashcards(self, deck_id: int, user_id: int):
        deck = self._deck_repository.get_users_deck_by_id(deck_id, user_id)

        if deck is None:
            raise LookupError("Deck not found")

        return self._flashcard_repository.list_flashcards(deck_id, user_id)

    def get_flashcard(self, flashcard_id: int, deck_id: int, user_id: int):
        deck = self._deck_repository.get_users_deck_by_id(deck_id, user_id)

        if deck is None:
            raise LookupError("Deck not found")

        flashcard = self._flashcard_repository.get_flashcard(
            flashcard_id, deck_id, user_id
        )

        if flashcard is None:
            raise LookupError("Flashcard not found")

        return flashcard

    def update_flashcard(
        self,
        updates: FlashcardInUpdate,
        flashcard_id: int,
        deck_id: int,
        user_id: int,
    ) -> Flashcard:
        deck = self._deck_repository.get_users_deck_by_id(deck_id, user_id)

        if deck is None:
            raise LookupError("Deck not found")

        flashcard = self._flashcard_repository.get_flashcard(
            flashcard_id, deck.id, user_id
        )

        if flashcard is None:
            raise LookupError("Flashcard not found")

        update_flashcard = self._flashcard_repository.update_flashcard(
            flashcard, updates.model_dump(exclude_none=True)
        )

        return update_flashcard

    def delete_flashcard(self, flashcard_id: int, deck_id: int, user_id: int):
        deck = self._deck_repository.get_users_deck_by_id(deck_id, user_id)

        if deck is None:
            raise LookupError("Deck not found")

        flashcard = self._flashcard_repository.get_flashcard(
            flashcard_id, deck_id, user_id
        )

        if flashcard is None:
            raise LookupError("Flashcard not found")

        return self._flashcard_repository.delete_flashcard(flashcard)
