from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.user import User
from app.db.schemas.flashcard import FlashcardInCreate
from app.core.security.dependencies import get_current_user

router = APIRouter()


@router.post("/")
def create_flashcard(
    data: FlashcardInCreate,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    pass


@router.get("/{flashcard_id}")
def get_flashcard(
    flashcard_id: int,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    pass


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
