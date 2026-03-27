def test_list_decks(access_token, deck, client):
    response = client.get(
        "/decks/", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    decks = response.json()
    for deck in decks:
        assert isinstance(deck["id"], int)
