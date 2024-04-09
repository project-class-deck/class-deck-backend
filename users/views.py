from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import CustomUser
from .serializers import UserRegistrationSerializer

class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
