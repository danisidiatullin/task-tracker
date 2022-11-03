from fastapi.testclient import TestClient


def auth_headers_developer(client: TestClient, json_user_developer):

    response = client.post(
        "/login/",
        json={
            "username": json_user_developer["username"],
            "password": json_user_developer["password"],
        },
    )
    data = response.json()

    return {"Authorization": f'Bearer {data["token"]}'}


def auth_headers_manager(client: TestClient, json_user_manager):
    client.post(
        "/signup/",
        json=json_user_manager,
    )

    response = client.post(
        "/login/",
        json={
            "username": json_user_manager["username"],
            "password": json_user_manager["password"],
        },
    )
    data = response.json()

    return {"Authorization": f'Bearer {data["token"]}'}
