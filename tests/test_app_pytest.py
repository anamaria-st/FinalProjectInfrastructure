import pytest
from app import create_app
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Username" in response.data
    assert b"Password" in response.data


def test_login_success(client):
    response = client.post(
        "/login",
        data={"username": "admin", "password": "secret"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Logged in successfully" in response.data


def test_login_failure(client):
    response = client.post(
        "/login",
        data={"username": "wrong", "password": "wrong"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data
