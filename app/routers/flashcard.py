from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.user import User
from app.db.schemas.flashcard import FlashcardInCreate, FlashcardOut
from app.core.security.dependencies import get_current_user
from app.service.flashcard import FlashcardService

router = APIRouter()


@router.post("/", response_model=FlashcardOut, status_code=200)
def create_flashcard(
    flashcard_data: FlashcardInCreate,
    deck_id: int,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        return FlashcardService(session).create_flashcard(
            flashcard_data, deck_id, user.id
        )
    except LookupError:
        raise HTTPException(status_code=400, detail="Deck not found")


@router.get("/{flashcard_id}")
def get_flashcard(
    flashcard_id: int,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    pass


@router.get("/", response_model=list[FlashcardOut], status_code=200)
def list_flashcards(
    deck_id: int,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        return FlashcardService(session).list_flashcards(deck_id, user.id)
    except LookupError:
        raise HTTPException(status_code=404, detail="Deck not found")


@router.patch("/{flashcard_id}")
def update_flashcard(
    flashcard_id: int,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    pass


@router.delete("/{flashcard_id}")
def delete_flashcard(
    flashcard_id: int,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    pass
