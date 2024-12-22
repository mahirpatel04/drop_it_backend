import pytest
from app.schemas import CreateUserRequest
from tests.test_auth import auth_token

@pytest.mark.asyncio
async def test_create_drop(client, auth_token):
    payload = {
        "content": "A new drop!",
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/drop/create-drop", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == payload["content"]
