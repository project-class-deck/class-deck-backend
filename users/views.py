from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import StudentRegistrationSerializer, UserRegistrationSerializer


@extend_schema(tags=["auth"])
class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)


@extend_schema(tags=["auth"])
class StudentRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentRegistrationSerializer
    permission_classes = (AllowAny,)
