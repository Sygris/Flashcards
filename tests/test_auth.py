import pytest


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


def test_login_success(registered_user, client):
    login_response = client.post(
        "/auth/login", json={"email": "user@gmail.com", "password": "password"}
    )

    assert login_response.status_code == 200
    response_data = login_response.json()
    assert isinstance(response_data["token"], str)
    assert isinstance(response_data["refresh_token"], str)


def test_login_wrong_password(registered_user, client):
    login_response = client.post(
        "/auth/login", json={"email": "user@gmail.com", "password": "wrongPWD"}
    )

    assert login_response.status_code == 400
    response_data = login_response.json()
    assert response_data["detail"] == "Please check your Credentials"


def test_login_wrong_email(registered_user, client):
    login_response = client.post(
        "/auth/login", json={"email": "useer@gmail.com", "password": "password"}
    )

    assert login_response.status_code == 400
    response_data = login_response.json()
    assert response_data["detail"] == "Please create an Account"
