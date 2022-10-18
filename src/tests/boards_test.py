from starlette.testclient import TestClient

fake_board1 = {
    "title": "Board1",
}


def test_create_board(client: TestClient):
    response = client.post(
        "/boards/",
        json=fake_board1,
    )
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == fake_board1["title"]
    assert data["id"] is not None
