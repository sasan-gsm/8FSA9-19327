from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="landing_page"),
    path("admin/", admin.site.urls),
    path("api/auth/", include("core.users.api.urls")),
    path("api/bookings/", include("core.bookings.api.urls")),
]
