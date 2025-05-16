from django.db import models
from django.conf import settings
from typing import Dict, Any, Optional

from core.common.models import TimeStampedModel
from core.tables.models import Table


class Reservation(TimeStampedModel):
    """
    Model for a table reservation.
    """

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations",
    )

    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name="reservations",
    )

    seats_reserved = models.PositiveIntegerField(help_text="Number of seats reserved")

    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    reservation_date = models.DateField(help_text="Date of the reservation")

    reservation_time = models.TimeField(help_text="Time of the reservation")

    class Meta:
        ordering = ["-reservation_date", "-reservation_time"]
        # A table can't be double-booked for the same date and time
        unique_together = ["table", "reservation_date", "reservation_time", "status"]

    def __str__(self) -> str:
        return f"{self.user.email} - Table {self.table.table_number} - {self.reservation_date}"

    def cancel(self) -> bool:
        """
        Cancel  reservation.
        """
        if self.status == "cancelled":
            return False

        self.status = "cancelled"
        self.save()

        # Make the table available again
        self.table.is_available = True
        self.table.save()

        return True

    @classmethod
    def create_reservation(
        cls,
        user: settings.AUTH_USER_MODEL,
        people_count: int,
        reservation_date: str,
        reservation_time: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new reservation for a user and specific number of people.
        """
        # Find the best table for this reservation
        optimal_table_info = Table.find_optimal_table(people_count)

        if not optimal_table_info:
            return None

        table = optimal_table_info["table"]
        seats_allocated = optimal_table_info["seats_allocated"]
        price = optimal_table_info["price"]

        # Create reservation
        reservation = cls.objects.create(
            user=user,
            table=table,
            seats_reserved=seats_allocated,
            total_cost=price,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
            status="confirmed",
        )

        # Make the table unavailable
        table.is_available = False
        table.save()

        return {
            "reservation_id": reservation.id,
            "table_id": table.table_number,
            "seats_reserved": seats_allocated,
            "total_cost": price,
            "reservation_date": reservation_date,
            "reservation_time": reservation_time,
        }
