from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from core.bookings.models import Reservation
from core.tables.models import Table

User = get_user_model()


class BookingAPITest(TestCase):
    def setUp(self):
        Table.objects.all().delete()
        User.objects.all().delete()
        Reservation.objects.all().delete()

        self.user = User.objects.create_user(
            email="sassan@sassan.com",
            password="testpassword",
            username="sassan",
        )

        self.table = Table.objects.create(
            table_number=201,  # Using a unique table number for this test class
            seats=4,
            price_per_seat=10.00,
            is_available=True,
        )

        self.reservation = Reservation.objects.create(
            user=self.user,
            table=self.table,
            seats_reserved=4,
            total_cost=40.00,
            status="confirmed",
            reservation_date=date.today(),
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.book_url = reverse("bookings:book_table")
        self.cancel_url = reverse("bookings:cancel_reservation")
        self.reservations_url = reverse("bookings:user_reservations")

    def tearDown(self):
        Reservation.objects.all().delete()
        Table.objects.all().delete()
        User.objects.all().delete()

    def test_book_table_success(self):
        Reservation.objects.all().delete()
        Table.objects.create(
            table_number=202,  # Using a unique table number
            seats=6,
            price_per_seat=15.00,
            is_available=True,
        )
        tomorrow = date.today() + timedelta(days=1)
        data = {
            "people_count": 6,
            "reservation_date": tomorrow.isoformat(),
        }
        response = self.client.post(self.book_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("reservation_id", response.data)
        self.assertIn("table_id", response.data)
        self.assertIn("seats_reserved", response.data)
        self.assertIn("total_cost", response.data)

    def test_book_table_invalid_data(self):
        data = {
            "people_count": -1,
            "reservation_date": date.today().isoformat(),
        }
        response = self.client.post(self.book_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_reservation_success(self):
        data = {"reservation_id": self.reservation.id}
        response = self.client.post(self.cancel_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, "cancelled")

    def test_cancel_nonexistent_reservation(self):
        data = {"reservation_id": 999}
        response = self.client.post(self.cancel_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_access(self):
        client = APIClient()
        book_response = client.post(self.book_url, {}, format="json")
        cancel_response = client.post(self.cancel_url, {}, format="json")
        reservations_response = client.get(self.reservations_url)
        self.assertEqual(book_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(cancel_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            reservations_response.status_code, status.HTTP_401_UNAUTHORIZED
        )
