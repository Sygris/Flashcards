from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security.dependencies import get_current_user
from app.db.database import get_db
from app.db.models.user import User
from app.db.schemas.deck import DeckIn, DeckOut
from app.service.deck import DeckService

router = APIRouter()


@router.get("/", response_model=list[DeckOut], status_code=200)
def get_decks(
    session: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return DeckService(session).get_all_decks(user.id)


@router.post("/", response_model=DeckOut, status_code=201)
def create_deck(
    deck_data: DeckIn,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        return DeckService(session).create_deck(deck_data, user.id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Deck already exists")


@router.get("/{deck_id}", response_model=DeckOut, status_code=200)
def get_deck(
    deck_id: int,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return DeckService(session).get_deck_by_id(deck_id, user.id)


@router.patch("/{deck_id}", response_model=DeckOut, status_code=200)
def update_deck(
    deck_id: int,
    updates: DeckIn,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        return DeckService(session).update_deck(deck_id, user.id, updates)
    except LookupError:
        raise HTTPException(status_code=400, detail="Deck not found")


@router.delete("/{deck_id}")
def delete_deck(
    deck_id: int,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        return DeckService(session).delete_deck(deck_id, user.id)
    except LookupError:
        raise HTTPException(status_code=400, detail="Deck not found")
