from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from core.users.api.views import (
    CustomTokenObtainPairView,
    LogoutView,
    UserProfileView,
)

app_name = "users"

urlpatterns = [
    # Authentication endpoints
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # User profile endpoints
    path("profile/", UserProfileView.as_view(), name="profile"),
]
