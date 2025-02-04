import os, sys
from fastapi.testclient import TestClient
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from main import app

load_dotenv(find_dotenv())
API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY")

client = TestClient(app)


def test_hello_success():
    response = client.post("/hello", headers={API_KEY_NAME: API_KEY})
    assert response.status_code == 200
    assert response.json() == {"message": "LIA API is running!"}


def test_hello_missing_api_key():
    response = client.post("/hello")
    assert response.status_code == 403  # Assuming 403 Forbidden for missing API key


def test_hello_invalid_api_key():
    response = client.post("/hello", headers={API_KEY_NAME: "invalid_api_key"})
    assert response.status_code == 401
