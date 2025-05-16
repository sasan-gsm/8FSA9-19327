from django.test import TestCase
from core.users.models import User
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status


class UserModelTest(TestCase):
    def test_create_user_with_email(self):
        user = User.objects.create_user(
            email="sassan@sassan.com", password="testpassword"
        )
        self.assertEqual(user.email, "sassan@sassan.com")
        self.assertTrue(user.check_password("testpassword"))

    def test_str_representation(self):
        user = User.objects.create_user(email="strtest@example.com", password="pass")
        self.assertEqual(str(user), "strtest@example.com")


class UserViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com", password="strongpassword", name="Test User"
        )
        self.client = APIClient()

    def test_token_obtain(self):
        url = reverse("users:login")
        response = self.client.post(
            url, {"email": "user@test.com", "password": "strongpassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_user_profile_view_get(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_logout_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("users:logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Successfully logged out")
