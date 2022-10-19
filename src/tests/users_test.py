from fastapi.testclient import TestClient
from sqlmodel import Session


def test_create_user(client: TestClient, user):
    response = client.post(
        "/signup/",
        json=user,
    )
    data = response.json()

    assert response.status_code == 201
    assert data["username"] == user["username"]
    assert data["email"] == user["email"]
    assert data["role"] == user["role"]


def test_login_user(session: Session, client: TestClient, user):
    client.post(
        "/signup/",
        json=user,
    )

    response = client.post(
        "/login/",
        json={
            "username": user["username"],
            "password": user["password"],
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert "token" in data


def test_users_me(session: Session, client: TestClient, user, auth_headers):
    response = client.get(
        "/users/me/",
        headers=auth_headers,
    )
    data = response.json()
    assert response.status_code == 200
    assert data["username"] == user["username"]
    assert data["email"] == user["email"]
    assert data["role"] == user["role"]
