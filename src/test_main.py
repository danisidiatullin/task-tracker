import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from models import get_session

fake_task1 = {
    "title": "Task1",
    "description": "about Task1",
    "status": "started",
    "priority": 20,
    "progress": 80,
}

fake_task2 = {
    "title": "Task2",
    "description": "about Task2",
    "status": "started",
}


@pytest.fixture(name="session")  #
def session_fixture():  #
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session  #


# client = TestClient(app)


def test_create_task(session: Session):
    def get_session_override():
        return session  #

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)

    response = client.post(
        "/tasks",
        json=fake_task1,
    )
    app.dependency_overrides.clear()
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == fake_task1["title"]
    assert data["description"] == fake_task1["description"]
    assert data["priority"] == fake_task1["priority"]
    assert data["progress"] == fake_task1["progress"]
    assert data["id"] is not None


def test_create_task_with_defaults(session: Session):
    def get_session_override():
        return session  #

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)

    response = client.post(
        "/tasks",
        json=fake_task2,
    )
    app.dependency_overrides.clear()
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == fake_task2["title"]
    assert data["description"] == fake_task2["description"]
    assert data["priority"] == 10
    assert data["progress"] == 0
    assert data["id"] is not None


def test_get_tasks_list(session: Session):
    def get_session_override():
        return session  #

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)

    client.post(
        "/tasks",
        json=fake_task1,
    )
    client.post(
        "/tasks",
        json=fake_task2,
    )

    response = client.get(
        "/tasks",
    )
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2


def test_root():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == [1, 2, 3]
