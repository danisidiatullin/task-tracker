from fastapi.testclient import TestClient

from main import app


def test_create_task():
    client = TestClient(app)

    response = client.post(
        "/tasks",
        json={
            "title": "Task1",
            "description": "about Task1",
            "status": "started",
            "priority": 20,
            "progress": 80,
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Task1"
    assert data["description"] == "about Task1"
    assert data["priority"] == 20
    assert data["progress"] == 80
    assert data["id"] is not None
