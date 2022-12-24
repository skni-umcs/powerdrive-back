from tests.test_api import client


def test_create_user():
    response = client.post(
        "/user",
        json={
            "username": "string",
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com",
            "password": "String1."
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "username": "string",
        "first_name": "string",
        "last_name": "string",
        "email": "user@example.com",
    }
