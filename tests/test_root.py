from fastapi import status
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Welcome to the boilerplate API"

def test_probe():
    response = client.get("/probe")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "I am the Python FastAPI API responding"
