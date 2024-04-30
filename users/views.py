from dj_rest_auth.jwt_auth import set_jwt_cookies
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import GuestRegistrationSerializer, UserRegistrationSerializer


@extend_schema(tags=["auth"])
class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        set_jwt_cookies(response, response.data["access"], response.data["refresh"])

        return response


@extend_schema(tags=["auth"])
class GuestRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = GuestRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        set_jwt_cookies(response, response.data["access"], response.data["refresh"])

        return response
