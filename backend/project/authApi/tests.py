from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser


# To run the test, write python manage.py test in the terminal.
class TestAuthAPi(TestCase):
    def test_testname(self):
        self.assertEqual(1, 1)


class AuthTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test", password="mypassword"
        )

    def test_registration_username_already_exist(self):
        data = {
            "username": "test",
            "first_name": "as",
            "last_name": "last",
            "email": "23425",
            "password": "mypassword",
            "user_type": "student",
            "roll_no": "43564",
        }

        response = self.client.post("/api-auth/register/", data)
        self.assertEqual(response.data["status"], 400)
        self.assertEqual(response.data["message"], "Username already exists")

    def test_registration_success(self):
        data = {
            "username": "test1",
            "first_name": "as",
            "last_name": "last",
            "email": "23425",
            "password": "mypassword1",
            "user_type": "student",
            "roll_no": "43564",
        }

        response = self.client.post("/api-auth/register/", data)
        self.assertEqual(response.status_code, 200)

    def test_login_wrong_password(self):
        data = {
            "username": "test",
            "password": "mypassword1",
        }

        response = self.client.post("/api-auth/login/", data)
        self.assertEqual(response.data["message"], "Invalid Credentials")

    def test_login_success(self):
        data = {
            "username": "test",
            "password": "mypassword",
        }

        response = self.client.post("/api-auth/login/", data)
        self.assertEqual(response.status_code, 200)

    def test_is_logged_in_without_token(self):
        response = self.client.get("/api-auth/is-logged-in/")
        self.assertEqual(response.data["message"], "User is not logged in.")

    def test_is_logged_in_with_token(self):
        data = {
            "username": "test",
            "password": "mypassword",
        }

        response = self.client.post("/api-auth/login/", data)
        self.assertEqual(response.status_code, 200)
        token = response.data["access"]
        response = self.client.get(
            "/api-auth/is-logged-in/", HTTP_AUTHORIZATION="Bearer " + token
        )
        self.assertEqual(response.data["message"], "User is logged in.")
