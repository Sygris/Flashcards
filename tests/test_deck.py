def test_create_deck_success(client, access_token):
    response = client.post(
        "/decks/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "title": "Test Create Deck",
            "description": "Deck created from test_create_deck_success",
        },
    )

    assert response.status_code == 201

    deck = response.json()
    assert isinstance(deck["id"], int)
    assert deck["title"] == "Test Create Deck"
    assert deck["description"] == "Deck created from test_create_deck_success"


def test_create_deck_duplicated(client, access_token, deck):
    response = client.post(
        "/decks/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "title": deck["title"],
            "description": deck["description"],
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Deck already exists"


def test_list_decks(client, access_token, deck):
    response = client.get(
        "/decks/", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    assert deck in response.json()


def test_get_deck(client, access_token, deck):
    response = client.get(
        f"/decks/{deck['id']}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    response_data = response.json()
    for key in response_data:
        assert response_data[key] == deck[key]


def test_get_deck_wrong_id(client, access_token, deck):
    response = client.get(
        f"/decks/{deck['id'] + 1}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Deck not found"


def test_update_deck_success(client, access_token, deck):
    response = client.patch(
        f"/decks/{deck['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"title": "Test Deck Update"},
    )

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["id"] == deck["id"]
    assert response_data["title"] == "Test Deck Update"
    assert response_data["description"] == deck["description"]


def test_update_deck_duplicated_title(client, access_token, deck):
    create_deck = client.post(
        "/decks/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "title": "Another Deck",
            "description": "Used to test updating to duplicated title",
        },
    )

    assert create_deck.status_code == 201
    assert create_deck.json()["title"] == "Another Deck"

    response = client.patch(
        f"/decks/{deck['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"title": create_deck.json()["title"]},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Deck already exists"


def test_delete_deck_success(client, access_token, deck):
    response = client.delete(
        f"/decks/{deck['id']}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    get_deck_response = client.get(
        f"/decks/{deck['id']}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert get_deck_response.status_code == 404
    assert get_deck_response.json()["detail"] == "Deck not found"
