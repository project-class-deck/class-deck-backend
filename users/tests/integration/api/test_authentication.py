import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from users.tests.factories.user_factory import UserFactory

User = get_user_model()


@pytest.mark.django_db
class TestUserAuthentication:
    def test_가입할_할_수_있다(self, client):
        response = client.post(
            reverse("user-register"),
            {
                "username": "testuser",
                "email": "test@test.com",
                "password": "testpassword1!",
                "nickname": "testnickname",
            },
            format="json",
        )

        assert response.status_code == 201
        assert response.data["username"] == "testuser"
        assert response.data["nickname"] == "testnickname"
        assert "access" in response.data
        assert "refresh" in response.data

        assert User.objects.filter(username="testuser").exists()
        test_user = User.objects.get(username="testuser")

        assert test_user.nickname == "testnickname"
        assert test_user.email == "test@test.com"
        assert test_user.is_active is True
        assert test_user.is_staff is False

    def test_닉네임_사용자는_닉네임만_입력해서_가입할_할_수_있다(self, client):
        response = client.post(
            reverse("student-register"),
            {
                "nickname": "studentnickname",
            },
            format="json",
        )

        assert response.status_code == 201
        assert response.data["nickname"] == "studentnickname"
        assert "access" in response.data
        assert "refresh" in response.data

        assert User.objects.filter(nickname="studentnickname").exists()
        test_user = User.objects.get(nickname="studentnickname")

        assert test_user.is_active is True
        assert test_user.is_staff is False

    def test_닉네임_사용자는_닉네임을_중복해서_가입할_할_수_있다(self, client):
        response = client.post(
            reverse("student-register"),
            {
                "nickname": "studentnickname",
            },
            format="json",
        )

        assert response.status_code == 201
        assert response.data["nickname"] == "studentnickname"
        assert "access" in response.data
        assert "refresh" in response.data

        assert User.objects.filter(nickname="studentnickname").exists()

        response = client.post(
            reverse("student-register"),
            {
                "nickname": "studentnickname",
            },
            format="json",
        )

        assert response.status_code == 201
        assert response.data["nickname"] == "studentnickname"
        assert "access" in response.data
        assert "refresh" in response.data

        assert User.objects.filter(nickname="studentnickname").count() == 2

    def test_사용자는_올바른_인증으로_로그인을_할_수_있다(self, client):
        User.objects.create_user(
            username="john", email="john@example.com", password="s3cr3t"
        )

        url = reverse("rest_login")

        data = {"username": "john", "password": "s3cr3t"}

        response = client.post(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

        login_user = response.data["user"]
        assert login_user["username"] == "john"
        assert login_user["email"] == "john@example.com"

        assert User.objects.filter(username="john").exists()

    def test_사용자는_올바르지_않은_인증으로는_로그인을_할_수_없다(self, client):
        url = reverse("rest_login")

        data = {"username": "john", "password": "wrongpassword"}

        response = client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data

    def test_닉네임_사용자는_비밀번호_없이도_인증정보를_제공할_수_있다(self, client):
        User.objects.create_user(
            username="john", email="john@example.com", password="s3cr3t"
        )

        response = client.post(
            reverse("student-register"),
            {
                "nickname": "studentnickname",
            },
            format="json",
        )

        access = response.data["access"]

        response = client.get(
            reverse("rest_user_details"), HTTP_AUTHORIZATION=f"Bearer {access}"
        )

        assert response.status_code == status.HTTP_200_OK

        assert response.data["nickname"] == "studentnickname"
        assert "username" in response.data
        assert "email" in response.data

    def test_사용자는_자신의_정보를_요청할_수_있다(self, set_credentials):
        user = UserFactory(username="john", email="john@example.com", nickname="john")

        client = set_credentials(user)

        url = reverse("rest_user_details")

        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == "john"
        assert response.data["nickname"] == "john"
