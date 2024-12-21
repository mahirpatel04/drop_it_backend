import pytest
from app.schemas import CreateUserRequest

@pytest.fixture
def auth_token(client):
    # Create a test user
    user_payload = {
        "username": "test_user123",
        "email": "test_user123@example.com",
        "password": "test_password",
        "first_name": "Test",
        "birthdate": "1990-01-01",
        "private": False # Adjust based on schema
}

    response = client.post("/auth/create-user", json=user_payload)
    assert response.status_code == 200

    # Login to get the token
    response = client.post(
        "/auth/token",
        data={"username": "test_user", "password": "test_password"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_create_user(client):
    payload = {
        "username": "test_user",
        "email": "test_user@example.com",
        "password": "test_password",
        "first_name": "Test",
        "birthdate": "1990-01-01",
        "private": False # Adjust based on schema
}

    response = client.post("/auth/create-user", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]