import re
import uuid

import dj_rest_auth.serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Guest

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "nickname")

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value

    def validate_password(self, value):
        # 영문 소문자, 대문자, 숫자, 특수문자 중 두 가지 이상 조합
        regex = r"^(?=.*[a-zA-Z])(?=.*[\d|!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$"
        if not re.match(regex, value):
            raise serializers.ValidationError(
                "비밀번호는 영문자, 숫자, 특수문자 중 두 가지 이상을 포함해야 합니다."
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            nickname=validated_data["nickname"],
            password=validated_data["password"],
        )
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        refresh = RefreshToken.for_user(instance)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class GuestRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ("id", "nickname")

    def create(self, validated_data):
        user = Guest.objects.create_user(
            username=uuid.uuid4().hex[:30],
            nickname=validated_data["nickname"],
        )
        user.set_unusable_password()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        refresh = RefreshToken.for_user(instance)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "nickname")
        read_only_fields = ("id", "username", "email")


class UserLoginSerializer(dj_rest_auth.serializers.LoginSerializer):
    email = None
