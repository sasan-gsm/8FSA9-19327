from django.urls import path
from core.bookings.api.views import (
    BookTableAPIView,
    CancelReservationAPIView,
    UserReservationsListAPIView,
)

app_name = "bookings"

urlpatterns = [
    # Action 1: Returns reservation details (cost, table ID, and number of seats)
    path("book/", BookTableAPIView.as_view(), name="book_table"),
    # Action 2: Cancels a reservation
    path("cancel/", CancelReservationAPIView.as_view(), name="cancel_reservation"),
    path(
        "reservations/", UserReservationsListAPIView.as_view(), name="user_reservations"
    ),
]
