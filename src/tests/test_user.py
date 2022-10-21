from fastapi.testclient import TestClient
from sqlmodel import Session


def test_create_user(client: TestClient, json_user):
    response = client.post(
        "/signup/",
        json=json_user,
    )
    data = response.json()

    assert response.status_code == 201
    assert data["username"] == json_user["username"]
    assert data["email"] == json_user["email"]
    assert data["role"] == json_user["role"]
    assert data["id"] is not None


def test_login_user(session: Session, client: TestClient, json_user):
    client.post(
        "/signup/",
        json=json_user,
    )

    response = client.post(
        "/login/",
        json={
            "username": json_user["username"],
            "password": json_user["password"],
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert "token" in data


def test_users_me(session: Session, client: TestClient, json_user, auth_headers):
    response = client.get(
        "/users/me/",
        headers=auth_headers,
    )
    data = response.json()
    assert response.status_code == 200
    assert data["username"] == json_user["username"]
    assert data["email"] == json_user["email"]
    assert data["role"] == json_user["role"]
