from django.urls import path

from .views import StudentRegistrationAPIView, UserRegistrationAPIView

urlpatterns = [
    path("auth/register/", UserRegistrationAPIView.as_view(), name="user-register"),
    path(
        "auth/register/student/",
        StudentRegistrationAPIView.as_view(),
        name="student-register",
    ),
]
