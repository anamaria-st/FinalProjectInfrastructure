import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app
@pytest.fixture
def client():
    # Crear la aplicación con configuración de testing
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client 


def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Username" in response.data
    assert b"Password" in response.data


def test_login_success(client):
    from app.models import User, db

    # Crear usuario dentro del contexto de la aplicación
    with client.application.app_context():
        user = User(username="admin")
        user.set_password("secret")
        db.session.add(user)
        db.session.commit()

    # Intentar login
    response = client.post(
        "/login",
        data={"username": "admin", "password": "secret"},
        follow_redirects=True,
    )

    # Debe redirigir al dashboard (200 tras redirect)
    assert response.status_code == 200
    assert b"Dashboard" in response.data or b"dashboard" in response.data



def test_login_failure(client):
    response = client.post(
        "/login",
        data={"username": "wrong", "password": "wrong"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data
