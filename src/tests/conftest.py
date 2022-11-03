import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from db import get_session
from main import app
from models import User, UserCreate


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


@pytest.fixture(name="json_user_developer", scope="function")
def json_user_developer_fixture(session: Session):
    fake_user1 = {
        "username": "danis1",
        "password": "danis1",
        "password2": "danis1",
        "email": "danis1@example.com",
        "role": "developer",
    }
    return fake_user1


@pytest.fixture(name="json_user_developer2", scope="function")
def json_user_developer2_fixture(session: Session):
    fake_user1 = {
        "username": "danis3",
        "password": "danis3",
        "password2": "danis3",
        "email": "danis3@example.com",
        "role": "developer",
    }
    return fake_user1


@pytest.fixture(name="json_user_manager", scope="function")
def json_user_manager_fixture(session: Session):
    fake_user1 = {
        "username": "danis2",
        "password": "danis2",
        "password2": "danis2",
        "email": "danis2@example.com",
        "role": "manager",
    }
    return fake_user1


@pytest.fixture(name="json_user_manager2", scope="function")
def json_user_manager2_fixture(session: Session):
    fake_user1 = {
        "username": "danis4",
        "password": "danis4",
        "password2": "danis4",
        "email": "danis4@example.com",
        "role": "manager",
    }
    return fake_user1


@pytest.fixture(name="json_task", scope="function")
def json_task_fixture(session: Session):
    task = {
        "title": "Task1",
        "description": "about Task1",
        "status": "started",
        "priority": 20,
        "progress": 80,
    }
    return task


@pytest.fixture(name="json_task_defaults", scope="function")
def json_task_defaults_fixture():
    task = {
        "title": "Task2",
        "description": "about Task2",
        "status": "started",
    }
    return task


@pytest.fixture(name="json_task_wrong_data", scope="function")
def json_task_wrong_data_fixture():
    task = {
        "title": "Task2",
        "description": "about Task2",
        "status": "start",
    }
    return task


@pytest.fixture(name="json_board", scope="function")
def json_board_fixture(session: Session):
    board = {
        "title": "Board1",
    }

    return board


# @pytest.fixture(name="db_user", scope="function")
# def db_user_fixture(session: Session):
#    user = UserCreate(
#        username="danis1", password="danis1", password2="danis1", email="danis1@example.com", role="developer"
#    )
#    db_user = User.from_orm(user)
#    # session.add(db_user)
#    # session.commit()
#    # session.refresh(db_user)
#    return db_user
