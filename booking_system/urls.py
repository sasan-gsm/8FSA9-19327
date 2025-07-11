from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Booking System API",
        default_version="v1",
        description="API documentation for the Booking System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="sasan.gsm@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="landing_page"),
    path("admin/", admin.site.urls),
    path("api/auth/", include("core.users.api.urls")),
    path("api/bookings/", include("core.bookings.api.urls")),
    # Swagger UI URLs
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
