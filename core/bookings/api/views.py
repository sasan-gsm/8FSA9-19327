from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import Any

from core.bookings.api.serializers import (
    BookingRequestSerializer,
    BookingResponseSerializer,
    CancelReservationSerializer,
    ReservationSerializer,
)
from core.bookings.services import ReservationService


class BookTableAPIView(APIView):
    """
    API view for booking a table.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Any) -> Response:
        serializer = BookingRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        people_count = serializer.validated_data["people_count"]
        reservation_date = serializer.validated_data["reservation_date"]
        reservation_time = serializer.validated_data["reservation_time"]

        service = ReservationService()
        result = service.book_table(
            user=request.user,
            people_count=people_count,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
        )

        if not result:
            return Response(
                {"error": "No table available"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = BookingResponseSerializer(data=result)
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CancelReservationAPIView(APIView):
    """
    API view for cancelling a reservation.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Any) -> Response:
        """
        Cancel a reservation.
        """
        serializer = CancelReservationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        reservation_id = serializer.validated_data["reservation_id"]

        service = ReservationService()
        result = service.cancel_reservation(
            reservation_id=reservation_id, user=request.user
        )

        if not result["success"]:
            return Response(
                {"error": result["message"]}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"message": result["message"]}, status=status.HTTP_200_OK)


class UserReservationsListAPIView(generics.ListAPIView):
    """
    API view for listing reservations.

    """

    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        service = ReservationService()
        return service.get_user_reservations(self.request.user)
