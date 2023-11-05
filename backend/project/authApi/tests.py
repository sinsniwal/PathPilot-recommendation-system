from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


# To run the test, write python manage.py test in the terminal.
class TestAuthAPi(TestCase):
    def test_testname(self):
        self.assertEqual(1, 1)
