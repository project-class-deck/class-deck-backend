from drf_spectacular.utils import extend_schema
from rest_framework import generics

from .models import User
from .serializers import StudentRegistrationSerializer, UserRegistrationSerializer


@extend_schema(tags=["auth"])
class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


@extend_schema(tags=["auth"])
class StudentRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentRegistrationSerializer
