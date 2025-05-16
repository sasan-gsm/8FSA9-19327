from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from typing import Any

from core.users.api.serializers import UserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view that uses our serializer class.
    """

    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Any) -> Response:
        # In a stateless JWT implementation, we don't need to do anything server-side
        # The client should discard the tokens
        return Response(
            {"message": "Successfully logged out"}, status=status.HTTP_200_OK
        )


class UserProfileView(APIView):
    """
    API view for retrieving and updating user profile information.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Any) -> Response:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request: Any) -> Response:
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
