from typing import Optional, Dict, Any
from django.db.models import QuerySet

from core.bookings.models import Reservation


class ReservationRepository:
    """
    Repository for Reservation model.
    """

    def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        """
        Get reservation by ID.
        """
        try:
            return Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            return None

    def get_user_reservations(self, user_id: int) -> QuerySet:
        """
        Get all reservations for user.
        """
        return Reservation.objects.filter(user_id=user_id)

    def create_reservation(self, data: Dict[str, Any]) -> Reservation:
        """
        Create reservation.
        """
        return Reservation.objects.create(**data)

    def update_reservation(
        self, reservation: Reservation, data: Dict[str, Any]
    ) -> Reservation:
        """
        Update reservation.
        """
        for key, value in data.items():
            setattr(reservation, key, value)
        reservation.save()
        return reservation

    def delete_reservation(self, reservation_id: int) -> bool:
        """
        Delete reservation by ID.
        """
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            reservation.delete()
            return True
        except Reservation.DoesNotExist:
            return False

    def cancel_reservation(self, reservation_id: int) -> Optional[Reservation]:
        """
        Cancel reservation by ID.
        """
        reservation = ReservationRepository.get_by_id(reservation_id)
        if reservation:
            reservation.cancel()
            return reservation
        return None
