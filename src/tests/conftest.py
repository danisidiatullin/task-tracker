import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from db import get_session
from main import app


@pytest.fixture(name="session", scope="function")
def session_fixture():
    engine = create_engine(
        "postgresql+psycopg2://postgres:postgres@localhost:5433/postgres_db",
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client", scope="function")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="user", scope="function")
def user_fixture():
    fake_user1 = {
        "username": "danis1",
        "password": "danis1",
        "password2": "danis1",
        "email": "danis1@example.com",
        "role": "developer",
    }
    return fake_user1


@pytest.fixture(name="auth_headers", scope="function")
def auth_headers_fixture(client: TestClient, user):
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

    return {"Authorization": f'Bearer {data["token"]}'}
