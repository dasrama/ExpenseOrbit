from app.schemas.user import CreateUserResponse
from fastapi import status
import pytest
from app.test.database import client


def test_create_user(client):
    response = client.post("/users/", json={"email": "hello@gmail.com", "password": "12345"})
    new_user = CreateUserResponse(**response.json())
    assert new_user.email == "hello@gmail.com"
    assert response.status_code ==  status.HTTP_201_CREATED


def test_login_user(client):
    response = client.post("/login", data={"username": "hello@gmail.com", "password": "12345"})
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "12345", 403),
    ("wrongemail@gmail.com", "wrongpassword", 403),
    ("hello@gmail.com", "wrongpassword", 403)
])
def test_incorrect_user(client, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code==status_code
   

