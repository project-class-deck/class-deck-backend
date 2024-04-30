import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status

from users.tests.factories import GuestFactory, UserFactory

User = get_user_model()


@pytest.mark.django_db
class TestUserAuthorization:
    def test_사용자로_가입하면_사용자_그룹에_속하게_된다(self, client):
        url = reverse("user-register")

        data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpassword1!",
            "nickname": "testnickname",
        }

        response = client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email=data["email"]).exists()

        user = User.objects.filter(email=data["email"]).get()
        user_group = Group.objects.get(name="User")
        assert user_group in user.groups.all()

    def test_게스트로_가입하면_게스트_그룹에_속하게_된다(self, client):
        url = reverse("guest-register")

        data = {
            "nickname": "testnickname",
        }

        response = client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(nickname=data["nickname"]).exists()

        user = User.objects.filter(nickname=data["nickname"]).get()
        user_group = Group.objects.get(name="Guest")
        assert user_group in user.groups.all()

    def test_사용자는_보드와_관련된_권한이_있다(self, set_credentials):
        user = UserFactory()

        assert user.has_perms(
            ["content.add_board", "content.change_board", "content.delete_board"]
        )

    def test_사용자는_게시물과_관련된_권한이_있다(self, set_credentials):
        user = UserFactory()

        assert user.has_perms(
            ["content.add_post", "content.change_post", "content.delete_post"]
        )

    def test_사용자는_댓글과_관련된_권한이_있다(self, set_credentials):
        user = UserFactory()

        assert user.has_perms(
            ["content.add_comment", "content.change_comment", "content.delete_comment"]
        )

    def test_게스트는_보드와_관련된_권한이_없다(self, set_credentials):
        guest = GuestFactory()

        assert not guest.has_perm("content.add_board")
        assert not guest.has_perm("content.change_board")
        assert not guest.has_perm("content.delete_board")

    def test_게스트는_게시물과_관련된_권한이_있다(self, set_credentials):
        guest = GuestFactory()

        assert guest.has_perms(
            ["content.add_post", "content.change_post", "content.delete_post"]
        )

    def test_게스트는_댓글과_관련된_권한이_있다(self, set_credentials):
        guest = GuestFactory()

        print(guest.get_all_permissions())

        assert guest.has_perms(
            ["content.add_comment", "content.change_comment", "content.delete_comment"]
        )
