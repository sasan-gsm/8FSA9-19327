from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, time
from unittest.mock import patch
from core.bookings.models import Reservation
from core.bookings.services import ReservationService
from core.tables.models import Table

User = get_user_model()


class ReservationServiceTest(TestCase):
    """Test cases for the ReservationService class."""

    def setUp(self):
        # test user
        self.user = User.objects.create_user(
            email="sassan@sassan.com",
            password="testpassword",
            username="sassan",
        )

        # test table
        self.table = Table.objects.create(
            table_number=1,
            seats=4,
            price_per_seat=10.00,
            is_available=True,
        )

        # test reservation
        self.reservation = Reservation.objects.create(
            user=self.user,
            table=self.table,
            seats_reserved=4,
            total_cost=40.00,
            status="confirmed",
            reservation_date=date.today(),
            reservation_time=time(19, 0),
        )

        self.service = ReservationService()

    @patch("core.bookings.models.Reservation.create_reservation")
    def test_book_table(self, mock_create_reservation):
        expected_result = {
            "reservation_id": 1,
            "table_id": 1,
            "seats_reserved": 4,
            "total_cost": 40.00,
            "reservation_date": date.today(),
            "reservation_time": time(19, 0),
        }
        mock_create_reservation.return_value = expected_result

        result = self.service.book_table(
            user=self.user,
            people_count=4,
            reservation_date=date.today(),
            reservation_time=time(19, 0),
        )

        self.assertEqual(result, expected_result)
        mock_create_reservation.assert_called_once_with(
            user=self.user,
            people_count=4,
            reservation_date=date.today(),
            reservation_time=time(19, 0),
        )

    def test_cancel_reservation_success(self):
        self.table.is_available = False
        self.table.save()

        result = self.service.cancel_reservation(
            reservation_id=self.reservation.id,
            user=self.user,
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Reservation cancelled")

        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, "cancelled")

        # Check table is available
        self.table.refresh_from_db()
        self.assertTrue(self.table.is_available)

    def test_cancel_reservation_not_found(self):
        result = self.service.cancel_reservation(
            reservation_id=999,
            user=self.user,
        )

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Reservation not found")

    def test_cancel_reservation_unauthorized(self):
        other_user = User.objects.create_user(
            email="notsassan@sassan.com",
            password="otherpassword",
            username="notsassan",
        )

        result = self.service.cancel_reservation(
            reservation_id=self.reservation.id,
            user=other_user,
        )

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "No permission cancel this reservation")

    def test_get_user_reservations(self):
        another_table = Table.objects.create(
            table_number=2,
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
            reservation_time=time(20, 0),  # 8:00 PM
        )
        reservations = self.service.get_user_reservations(self.user)

        self.assertEqual(len(reservations), 2)
        self.assertIn(self.reservation, reservations)
        self.assertIn(another_reservation, reservations)
