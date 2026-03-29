import os
import pytest
from fastapi.testclient import TestClient

os.environ["DB_NAME"] = "flashcards_test"
os.environ["DB_PORT"] = "5433"

from app.main import app
from app.db.database import SessionLocal
from app.db.models.deck import Deck
from app.db.models.flashcard import Flashcard
from app.db.models.user import User
from app.db.utils.init_db import create_tables


@pytest.fixture
def db_setup():
    create_tables()
    session = SessionLocal()
    yield session

    session.query(Flashcard).delete()
    session.query(Deck).delete()
    session.query(User).delete()

    session.commit()
    session.close()


@pytest.fixture
def client():
    client = TestClient(app)
    return client


@pytest.fixture
def registered_user(db_setup, client):
    response = client.post(
        "/auth/signup", json={"email": "user@gmail.com", "password": "password"}
    )
    if response.status_code != 201:
        pytest.fail("Failed to signup!")

    return response


@pytest.fixture
def access_token(registered_user, client):
    login_response = client.post(
        "/auth/login", json={"email": "user@gmail.com", "password": "password"}
    )

    if login_response.status_code != 200:
        pytest.fail("Failed to login!")

    return login_response.json()["token"]


@pytest.fixture
def deck(access_token, client):
    response = client.post(
        "/decks/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"title": "Fixtures", "description": "Deck created from conftest"},
    )

    if response.status_code != 201:
        pytest.fail("Failed to create deck!")

    return response.json()


@pytest.fixture
def flashcard(access_token, client, deck):
    response = client.post(
        f"/decks/{deck['id']}/flashcards/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"question": "What is 1+1", "answer": "2"},
    )

    if response.status_code != 201:
        pytest.fail("Failed to create flashcard!")

    return response.json()
