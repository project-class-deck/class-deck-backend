from django.urls import path

from .views import StudentRegistrationAPIView, UserRegistrationAPIView

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="user-register"),
    path(
        "register/student/",
        StudentRegistrationAPIView.as_view(),
        name="student-register",
    ),
]
