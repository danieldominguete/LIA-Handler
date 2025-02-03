from fastapi.testclient import TestClient
from main import app
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY")

client = TestClient(app)


def test_root():
    response = client.post("/hello", headers={"X-API-Key": API_KEY})
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
