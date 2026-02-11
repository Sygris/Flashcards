from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security.dependencies import get_current_user
from app.db.database import get_db
from app.db.models.user import User
from app.db.schemas.deck import DeckIn, DeckOut
from app.service.deck import DeckService

router = APIRouter()


@router.post("/create", response_model=DeckOut, status_code=200)
def create_deck(
    deck_data: DeckIn,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return DeckService(session).create_deck(deck_data, user)


@router.get("/{deck_id}", response_model=DeckOut, status_code=200)
def get_deck(
    deck_id: int,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return DeckService(session).get_deck_by_id(deck_id, user)


@router.get("/", response_model=list[DeckOut], status_code=200)
def get_decks(
    session: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return DeckService(session).get_all_decks(user)
