from typing import Optional, Dict, Any, List
from django.contrib.auth import get_user_model
from core.bookings.models import Reservation
from core.bookings.repositories import ReservationRepository

User = get_user_model()


class ReservationService:
    """
    Service class for reservation business logic.
    """

    def __init__(self):
        self.repository = ReservationRepository()

    def book_table(
        self,
        user: User,
        people_count: int,
        reservation_date: str,
        reservation_time: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Book a table for a user and number of people.
        """

        return Reservation.create_reservation(
            user=user,
            people_count=people_count,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
        )

    def cancel_reservation(self, reservation_id: int, user: User) -> Dict[str, Any]:
        """
        Cancel reservation.
        """
        reservation = self.repository.get_by_id(reservation_id)

        if not reservation:
            return {"success": False, "message": "Reservation not found"}

        if reservation.user != user:
            return {
                "success": False,
                "message": "You do not have permission to cancel this reservation",
            }

        success = reservation.cancel()

        if success:
            return {"success": True, "message": "Reservation cancelled successfully"}
        else:
            return {"success": False, "message": "Reservation is already cancelled"}

    def get_user_reservations(self, user: User) -> List[Reservation]:
        """
        get all reservations for a user.
        """
        return self.repository.get_user_reservations(user.id)

    def get_reservation_details(
        self, reservation_id: int, user: User
    ) -> Optional[Reservation]:
        """
        get a specific reservation.
        """
        reservation = self.repository.get_by_id(reservation_id)

        if reservation and reservation.user == user:
            return reservation

        return None
