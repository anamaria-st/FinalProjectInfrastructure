import unittest
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app

class LoginPageTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
        app.config["TESTING"] = True
        self.client = app.test_client()

    with app.app_context():
        db.create_all()

    def test_root_redirects_to_login(self):
        response = self.client.get("/")
        # Flask usa 302 en el redirect
        self.assertIn(response.status_code, (301, 302))

    def test_register_text_is_present(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Register now", response.data)


if __name__ == "__main__":
    unittest.main()
