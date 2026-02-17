from app.db.models.flashcard import Flashcard
from app.repository.deck import DeckRepository
from app.repository.flashcard import FlashcardRepository
from app.db.schemas.flashcard import FlashcardInCreate


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

        flashcard = Flashcard(**flashcard_data.model_dump(exclude_unset=True))
        flashcard.deck_id = deck.id

        return self._flashcard_repository.create_flashcard(flashcard)

    def list_flashcards(self, deck_id: int, user_id: int):
        deck = self._deck_repository.get_users_deck_by_id(deck_id, user_id)

        if deck is None:
            raise LookupError("Deck not found")

        return self._flashcard_repository.list_flashcards(deck_id)
