from fastapi import status
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.main import app
from app.schemas.user import CreateUserResponse
from app.database import settings, get_db, Base

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/expenseorbit_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TesingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TesingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)  
    Base.metadata.create_all(bind=engine)
    return TestClient(app=app)

# client = TestClient(app=app)

def test_user(client):
    response = client.post("/user/", json={"email": "hello@gmail.com", "password": "12345"})
    new_user = CreateUserResponse(**response.json())
    assert new_user.email == "hello@gmail.com"
    assert response.status_code ==  status.HTTP_201_CREATED

