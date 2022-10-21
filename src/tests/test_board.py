from starlette.testclient import TestClient


def test_create_board(client: TestClient, auth_headers, json_board):
    response = client.post(
        "/boards/",
        json=json_board,
        headers=auth_headers,
    )
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == json_board["title"]
    assert data["id"] is not None
