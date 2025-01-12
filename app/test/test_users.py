from app.schemas.user import CreateUserResponse
from fastapi import status
from app.test.database import client


def test_user(client):
    response = client.post("/user/", json={"email": "hello@gmail.com", "password": "12345"})
    new_user = CreateUserResponse(**response.json())
    assert new_user.email == "hello@gmail.com"
    assert response.status_code ==  status.HTTP_201_CREATED

