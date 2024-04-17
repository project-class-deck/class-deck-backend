from rest_framework import generics

from .models import User
from .serializers import StudentRegistrationSerializer, UserRegistrationSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class StudentRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentRegistrationSerializer
