def test_signup(db_setup, client):
    response = client.post(
        "/auth/signup", json={"email": "user@gmail.com", "password": "password"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user@gmail.com"
    assert isinstance(data["id"], int)
    assert data["nickname"] is None


def test_signup_duplicate_email(db_setup, client):
    response = client.post(
        "/auth/signup", json={"email": "user@gmail.com", "password": "password"}
    )

    response = client.post(
        "/auth/signup", json={"email": "user@gmail.com", "password": "password"}
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"
