def test_create_flashcard_success(client, access_token, deck):
    response = client.post(
        f"/decks/{deck['id']}/flashcards/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "question": "Is this flashcard being created in test_create_flashcard_success?",
            "answer": "Yes it is",
        },
    )

    assert response.status_code == 201

    flashcard = response.json()
    assert (
        flashcard["question"]
        == "Is this flashcard being created in test_create_flashcard_success?"
    )
    assert flashcard["answer"] == "Yes it is"


def test_create_flashcard_deck_not_found(client, access_token, deck):
    response = client.post(
        f"/decks/{deck['id'] + 1}/flashcards/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "question": "Is this flashcard being created in test_create_flashcard_success?",
            "answer": "Yes it is",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Deck not found"


def test_create_duplicated_flashcard(client, access_token, deck, flashcard):
    response = client.post(
        f"/decks/{deck['id']}/flashcards/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"question": flashcard["question"], "answer": flashcard["answer"]},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Flashcard already exists"


def test_list_flashcards(client, access_token, deck, flashcard):
    response = client.get(
        f"/decks/{deck['id']}/flashcards/",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert flashcard in response.json()


def test_list_flashcards_deck_not_found(client, access_token, deck):
    response = client.get(
        f"/decks/{deck['id'] + 1}/flashcards/",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Deck not found"


def test_get_flashcard(client, access_token, deck, flashcard):
    response = client.get(
        f"/decks/{deck['id']}/flashcards/{flashcard['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    response_data = response.json()
    for key in response_data:
        assert response_data[key] == flashcard[key]
