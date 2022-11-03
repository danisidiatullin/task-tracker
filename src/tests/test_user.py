from fastapi.testclient import TestClient
from sqlmodel import Session

from models.user import Role, User
from tests.utils import auth_headers_developer, auth_headers_manager


def test_create_user(client: TestClient, json_user_developer):
    response = client.post(
        "/signup/",
        json=json_user_developer,
    )
    data = response.json()

    assert response.status_code == 201
    assert data["username"] == json_user_developer["username"]
    assert data["email"] == json_user_developer["email"]
    assert data["role"] == json_user_developer["role"]
    assert data["id"] is not None


def test_login_user(session: Session, client: TestClient, json_user_developer):
    client.post(
        "/signup/",
        json=json_user_developer,
    )

    response = client.post(
        "/login/",
        json={
            "username": json_user_developer["username"],
            "password": json_user_developer["password"],
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert "token" in data


def test_users_me(session: Session, client: TestClient, json_user_developer, auth_headers_developer):
    response = client.get(
        "/users/me/",
        headers=auth_headers_developer,
    )
    data = response.json()
    assert response.status_code == 200
    assert data["username"] == json_user_developer["username"]
    assert data["email"] == json_user_developer["email"]
    assert data["role"] == json_user_developer["role"]


def test_change_user_role_developer_in_developer(
    session: Session, client: TestClient, json_user_developer, json_user_developer2
):
    response = client.post(
        "/signup/",
        json=json_user_developer,
    )
    user_developer = response.json()

    response = client.post(
        "/signup/",
        json=json_user_developer2,
    )
    user_developer2 = response.json()

    response = client.patch(
        f"/users/{user_developer['id']}/",
        json={"role": "manager"},
        headers=auth_headers_developer(client, json_user_developer2),
    )
    assert response.status_code == 403

    response = client.patch(
        f"/users/{user_developer2['id']}/",
        json={"role": "manager"},
        headers=auth_headers_developer(client, json_user_developer),
    )
    assert response.status_code == 403

    db_user_developer = session.get(User, user_developer["id"])
    db_user_developer2 = session.get(User, user_developer2["id"])

    assert db_user_developer.role == db_user_developer2.role == Role.developer


def test_change_user_role_developer_in_manager(
    session: Session, client: TestClient, json_user_developer, json_user_manager
):
    response = client.post(
        "/signup/",
        json=json_user_developer,
    )
    user_developer = response.json()

    response = client.post(
        "/signup/",
        json=json_user_manager,
    )
    user_manager = response.json()

    response = client.patch(
        f"/users/{user_manager['id']}/",
        json={"role": "developer"},
        headers=auth_headers_developer(client, json_user_developer),
    )
    assert response.status_code == 403

    db_user_manager = session.get(User, user_manager["id"])
    assert db_user_manager.role == Role.manager


def test_change_user_role_manager_in_developer(
    session: Session, client: TestClient, json_user_developer, json_user_manager
):
    response = client.post(
        "/signup/",
        json=json_user_developer,
    )
    user_developer = response.json()

    response = client.post(
        "/signup/",
        json=json_user_manager,
    )
    user_manager = response.json()

    response = client.patch(
        f"/users/{user_developer['id']}/",
        json={"role": "manager"},
        headers=auth_headers_manager(client, json_user_manager),
    )
    user_developer_patched = response.json()

    assert response.status_code == 200
    assert user_developer_patched["role"] == "manager"
    assert user_developer_patched["id"] == user_developer["id"]

    db_user_developer = session.get(User, user_developer["id"])
    assert db_user_developer.role == Role.manager


def test_change_user_role_manager_in_manager(
    session: Session, client: TestClient, json_user_manager, json_user_manager2
):
    response = client.post(
        "/signup/",
        json=json_user_manager,
    )
    user_manager = response.json()

    response = client.post(
        "/signup/",
        json=json_user_manager2,
    )
    user_manager2 = response.json()

    response = client.patch(
        f"/users/{user_manager['id']}/",
        json={"role": "developer"},
        headers=auth_headers_manager(client, json_user_manager2),
    )
    assert response.status_code == 422

    response = client.patch(
        f"/users/{user_manager2['id']}/",
        json={"role": "developer"},
        headers=auth_headers_manager(client, json_user_manager),
    )
    assert response.status_code == 422

    db_user_manager = session.get(User, user_manager["id"])
    db_user_manager2 = session.get(User, user_manager2["id"])
    assert db_user_manager.role == db_user_manager2.role == Role.manager
