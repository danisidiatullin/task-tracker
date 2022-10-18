import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from main import Task, app, get_session

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

fake_task3 = {
    "title": "Task2",
    "description": "about Task2",
    "status": "start",
}


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "postgresql+psycopg2://postgres:postgres@localhost:5433/postgres_db",
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_task(client: TestClient):
    response = client.post(
        "/tasks/",
        json=fake_task1,
    )
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == fake_task1["title"]
    assert data["description"] == fake_task1["description"]
    assert data["priority"] == fake_task1["priority"]
    assert data["progress"] == fake_task1["progress"]
    assert data["id"] is not None


def test_create_task_with_defaults(client: TestClient):
    response = client.post(
        "/tasks/",
        json=fake_task2,
    )
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == fake_task2["title"]
    assert data["description"] == fake_task2["description"]
    assert data["priority"] == 10
    assert data["progress"] == 0
    assert data["id"] is not None


def test_create_task_with_wrong_data(client: TestClient):
    response = client.post(
        "/tasks/",
        json=fake_task3,
    )
    data = response.json()

    assert response.status_code == 422


def test_get_tasks_list(session: Session, client: TestClient):
    task_1 = Task(**fake_task1)
    task_2 = Task(**fake_task2)

    session.add(task_1)
    session.add(task_2)
    session.commit()

    response = client.get(
        "/tasks",
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2


def test_delete_task(session: Session, client: TestClient):
    task_1 = Task(**fake_task1)
    session.add(task_1)

    response = client.get("/tasks/")
    data = response.json()
    assert len(data) == 1

    response = client.delete("/tasks/1/")
    assert response.status_code == 204

    response = client.get("/tasks")
    data = response.json()
    assert len(data) == 0


def test_delete_non_existent_task(session: Session, client: TestClient):
    task_1 = Task(**fake_task1)
    session.add(task_1)

    response = client.get("/tasks/")
    data = response.json()
    assert len(data) == 1

    response = client.delete("/tasks/2/")
    assert response.status_code == 404

    response = client.get("/tasks")
    data = response.json()
    assert len(data) == 1


def test_patch_task(session: Session, client: TestClient):
    task_1 = Task(**fake_task1)
    session.add(task_1)

    response = client.get("/tasks/1/")
    data = response.json()
    assert data["progress"] == fake_task1["progress"]

    response = client.patch("/tasks/1/", json={"progress": 98})
    data = response.json()
    assert data["progress"] != fake_task1["progress"]
    assert data["progress"] == 98
