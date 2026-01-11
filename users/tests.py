from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User, Business


class AuthTests(APITestCase):
    def setUp(self):
        self.business = Business.objects.create(name="TestBiz")
        self.user = User.objects.create_user(
            username="test",
            password="pass123",
            business=self.business
        )

    def test_jwt_auth_success(self):
        """
        Ensure a user can obtain JWT tokens with valid credentials.
        """
        url = reverse("users:token_obtain")
        response = self.client.post(url, {"username": "test", "password": "pass123"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_jwt_auth_failure(self):
        """
        Ensure authentication fails with invalid credentials.
        """
        url = reverse("users:token_obtain")
        response = self.client.post(url, {"username": "test", "password": "wrongpass"})
        self.assertEqual(response.status_code, 401)

