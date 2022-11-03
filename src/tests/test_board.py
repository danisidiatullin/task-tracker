from starlette.testclient import TestClient

from tests.utils import auth_headers_developer


def test_create_board(client: TestClient, json_board, json_user_developer):
    client.post(
        "/signup/",
        json=json_user_developer,
    )

    response = client.post(
        "/boards/",
        json=json_board,
        headers=auth_headers_developer(client, json_user_developer),
    )
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == json_board["title"]
    assert data["id"] is not None
