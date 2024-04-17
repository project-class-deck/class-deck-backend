import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

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


class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "nickname")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            nickname=validated_data["nickname"],
        )
        user.set_unusable_password()
        return user
