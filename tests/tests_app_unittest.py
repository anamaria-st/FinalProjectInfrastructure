import unittest
from app import create_app


class LoginPageTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config["TESTING"] = True
        self.client = app.test_client()

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
