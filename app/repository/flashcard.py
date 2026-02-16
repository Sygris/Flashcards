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
