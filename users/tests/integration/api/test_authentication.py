import pytest
from dj_rest_auth.tests.mixins import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from users.tests.conftest import set_credentials
from users.tests.factories.user_factory import UserFactory

User = get_user_model()


@pytest.mark.django_db
class TestUserAuthentication:

    @pytest.fixture
    def user(self):
        test_user = User.objects.create_user(
            username="john", email="john@example.com", password="s3cr3t"
        )
        return test_user

    @pytest.fixture
    def no_login(self):
        return APIClient()

    def test_가입할_할_수_있다(self, no_login):
        response = no_login.post(
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

    def test_학생은_닉네임만_입력해서_가입할_할_수_있다(self, no_login):
        response = no_login.post(
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

    def test_학생은_닉네임을_중복해서_가입할_할_수_있다(self, no_login):
        response = no_login.post(
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

        response = no_login.post(
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

    def test_사용자는_올바른_인증으로_로그인을_할_수_있다(self, user):
        client = APIClient()

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

    def test_사용자는_올바르지_않은_인증으로는_로그인을_할_수_없다(self, no_login):
        url = reverse("rest_login")

        data = {"username": "john", "password": "wrongpassword"}

        response = no_login.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data

    def test_학생은_비밀번호_없이도_인증정보를_제공할_수_있다(self, no_login, user):
        response = no_login.post(
            reverse("student-register"),
            {
                "nickname": "studentnickname",
            },
            format="json",
        )

        access = response.data["access"]

        response = no_login.get(
            reverse("rest_user_details"), HTTP_AUTHORIZATION=f"Bearer {access}"
        )

        assert response.status_code == status.HTTP_200_OK

        assert response.data["nickname"] == "studentnickname"
        assert "username" in response.data
        assert "email" in response.data

    def test_사용자는_자신의_정보를_요청할_수_있다(self):
        user = UserFactory(username="john", nickname="john")

        client = set_credentials(user)

        url = reverse("rest_user_details")

        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == "john"
        assert response.data["nickname"] == "john"
