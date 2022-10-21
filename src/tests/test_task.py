from fastapi.testclient import TestClient
from sqlmodel import Session

from models.task import Task


def test_create_task(client: TestClient, auth_headers, json_task):
    response = client.post(
        "/tasks/",
        json=json_task,
        headers=auth_headers,
    )
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == json_task["title"]
    assert data["description"] == json_task["description"]
    assert data["priority"] == json_task["priority"]
    assert data["progress"] == json_task["progress"]
    assert data["id"] is not None


def test_create_task_with_defaults(client: TestClient, auth_headers, json_task_defaults):
    response = client.post(
        "/tasks/",
        json=json_task_defaults,
        headers=auth_headers,
    )
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == json_task_defaults["title"]
    assert data["description"] == json_task_defaults["description"]
    assert data["priority"] == 10
    assert data["progress"] == 0
    assert data["id"] is not None


def test_create_task_with_wrong_data(client: TestClient, auth_headers, json_task_wrong_data):
    response = client.post(
        "/tasks/",
        json=json_task_wrong_data,
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_get_tasks_list(session: Session, client: TestClient, json_task, json_task_defaults):
    task_1 = Task(**json_task)
    task_2 = Task(**json_task_defaults)

    session.add(task_1)
    session.add(task_2)
    session.commit()

    response = client.get(
        "/tasks/",
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2


def test_delete_task(session: Session, client: TestClient, json_task):
    task_1 = Task(**json_task)
    session.add(task_1)

    response = client.get("/tasks/")
    data = response.json()
    assert len(data) == 1

    response = client.delete("/tasks/1/")
    assert response.status_code == 204

    response = client.get("/tasks/")
    data = response.json()
    assert len(data) == 0


def test_delete_non_existent_task(session: Session, client: TestClient, json_task):
    task_1 = Task(**json_task)
    session.add(task_1)

    response = client.get("/tasks/")
    data = response.json()
    assert len(data) == 1

    response = client.delete("/tasks/2/")
    assert response.status_code == 404

    response = client.get("/tasks")
    data = response.json()
    assert len(data) == 1


def test_patch_task(session: Session, client: TestClient, json_task):
    task_1 = Task(**json_task)
    session.add(task_1)

    response = client.get("/tasks/1/")
    data = response.json()
    assert data["progress"] == json_task["progress"]

    response = client.patch("/tasks/1/", json={"progress": 98})
    data = response.json()
    assert data["progress"] != json_task["progress"]
    assert data["progress"] == 98


def test_patch_with_status_task(session: Session, client: TestClient, json_task):
    task_1 = Task(**json_task)
    session.add(task_1)

    response = client.get("/tasks/1/")
    data = response.json()
    assert data["progress"] == json_task["progress"]
    assert data["status"] == json_task["status"]

    response = client.patch("/tasks/1/", json={"progress": 98, "status": "finished"})
    data = response.json()
    assert data["progress"] != json_task["progress"]
    assert data["progress"] == 98
    assert data["status"] != json_task["status"]
    assert data["status"] == "finished"
