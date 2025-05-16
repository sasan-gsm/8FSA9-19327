from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from unittest.mock import patch
from core.bookings.models import Reservation
from core.bookings.services import ReservationService
from core.tables.models import Table

User = get_user_model()


class ReservationServiceTest(TestCase):
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
            table_number=301,
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

        self.service = ReservationService()

    def tearDown(self):
        Reservation.objects.all().delete()
        Table.objects.all().delete()
        User.objects.all().delete()

    @patch("core.bookings.models.Reservation.create_reservation")
    def test_book_table(self, mock_create_reservation):
        expected_result = {
            "reservation_id": 1,
            "table_id": 1,
            "seats_reserved": 4,
            "total_cost": 40.00,
            "reservation_date": date.today(),
        }
        mock_create_reservation.return_value = expected_result
        result = self.service.book_table(
            user=self.user,
            people_count=4,
            reservation_date=date.today(),
        )
        self.assertEqual(result, expected_result)
        mock_create_reservation.assert_called_once_with(
            user=self.user,
            people_count=4,
            reservation_date=date.today(),
        )

    def test_cancel_reservation_not_found(self):
        result = self.service.cancel_reservation(
            reservation_id=999,
            user=self.user,
        )
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Reservation not found")

    def test_get_user_reservations(self):
        another_table = Table.objects.create(
            table_number=302,  # Using a unique table number
            seats=6,
            price_per_seat=15.00,
            is_available=True,
        )
        another_reservation = Reservation.objects.create(
            user=self.user,
            table=another_table,
            seats_reserved=6,
            total_cost=90.00,
            status="confirmed",
            reservation_date=date.today(),
        )
        reservations = self.service.get_user_reservations(self.user)
        self.assertEqual(len(reservations), 2)
        self.assertIn(self.reservation, reservations)
        self.assertIn(another_reservation, reservations)
