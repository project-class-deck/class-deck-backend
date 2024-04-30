from django.urls import path

from .views import GuestRegistrationAPIView, UserRegistrationAPIView

urlpatterns = [
    path("auth/register/", UserRegistrationAPIView.as_view(), name="user-register"),
    path(
        "auth/register/guest/",
        GuestRegistrationAPIView.as_view(),
        name="guest-register",
    ),
]
