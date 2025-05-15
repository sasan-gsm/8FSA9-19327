from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from core.common.models import TimeStampedModel


class Table(TimeStampedModel):
    """
    Restaurant table model.
    """

    table_number = models.PositiveIntegerField(
        unique=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    seats = models.PositiveIntegerField(
        validators=[MinValueValidator(4), MaxValueValidator(10)],
    )

    price_per_seat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["table_number"]

    def __str__(self) -> str:
        return f"Table {self.table_number} ({self.seats} seats)"
