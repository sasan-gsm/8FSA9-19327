from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.users.backends import CustomAuthenticationBackend

User = get_user_model()


class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "sassan@sassan.com",
            "username": "sassan",
            "password": "testpassword123",
            "name": "Test User",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertEqual(self.user.username, self.user_data["username"])
        self.assertEqual(self.user.name, self.user_data["name"])
        self.assertTrue(self.user.check_password(self.user_data["password"]))

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email="admin@admin.com",
            password="adminpass123",
            username="admin",
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

    def test_email_normalized(self):
        User.objects.all().delete()
        email = "test@EXAMPLE.COM"
        user = User.objects.create_user(email=email, password="test123")
        self.assertEqual(user.email, email.lower())

    def test_email_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="test123")


class CustomAuthBackendTests(TestCase):
    def setUp(self):
        self.backend = CustomAuthenticationBackend()
        self.user = User.objects.create_user(
            email="sassan@sassan.com",
            username="sassan",
            password="pass123",
        )

    def test_authenticate_with_email(self):
        authenticated_user = self.backend.authenticate(
            None, username="sassan@sassan.com", password="pass123"
        )
        self.assertEqual(authenticated_user, self.user)

    def test_authenticate_with_username(self):
        authenticated_user = self.backend.authenticate(
            None, username="sassan", password="pass123"
        )
        self.assertEqual(authenticated_user, self.user)

    def test_authenticate_invalid_credentials(self):
        self.assertIsNone(
            self.backend.authenticate(
                None, username="sassan@sassan.com", password="wrongpass"
            )
        )
        self.assertIsNone(
            self.backend.authenticate(
                None, username="wrong@example.com", password="pass123"
            )
        )


class UserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="sassan@sassan.com",
            username="sassan",
            password="pass123",
            name="API User",
        )
        self.client.force_authenticate(user=self.user)

    def test_user_profile_get(self):
        url = reverse("users:profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["username"], self.user.username)

    def test_user_profile_update(self):
        url = reverse("users:profile")
        payload = {"first_name": "Updated", "last_name": "Name"}
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload["first_name"])
        self.assertEqual(self.user.last_name, payload["last_name"])
