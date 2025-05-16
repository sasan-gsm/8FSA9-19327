from rest_framework import serializers
from core.bookings.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    """Serializer for the Reservation model."""

    class Meta:
        model = Reservation
        fields = [
            "id",
            "table",
            "seats_reserved",
            "total_cost",
            "status",
            "reservation_date",
            "reservation_time",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class BookingRequestSerializer(serializers.Serializer):
    """Serializer for booking request data."""

    people_count = serializers.IntegerField(min_value=1)
    reservation_date = serializers.DateField()
    reservation_time = serializers.TimeField()

    def validate_people_count(self, value: int) -> int:
        if value <= 0:
            raise serializers.ValidationError("Number of people must be positive")
        return value


class BookingResponseSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()
    table_id = serializers.IntegerField()
    seats_reserved = serializers.IntegerField()
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    reservation_date = serializers.DateField()
    reservation_time = serializers.TimeField()


class CancelReservationSerializer(serializers.Serializer):
    """Serializer for cancellation"""

    reservation_id = serializers.IntegerField()

    def validate_reservation_id(self, value: int) -> int:
        try:
            Reservation.objects.get(id=value)
        except Reservation.DoesNotExist:
            raise serializers.ValidationError("Reservation does not exist")
        return value
