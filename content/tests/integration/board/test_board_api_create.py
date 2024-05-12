import pytest
from django.urls import reverse
from rest_framework import status

from users.tests.factories import GuestFactory, UserFactory


@pytest.mark.django_db
class TestBoardCreateAPI:
    def test_비로그인_사용자는_보드를_만들_수_없다(self, client):
        url = reverse("boards-list")

        data = {"title": "test_board", "description": "test_board"}

        response = client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_로그인_사용자는_보드를_만들_수_있다(self, set_credentials):
        user = UserFactory()

        user_client = set_credentials(user)

        url = reverse("boards-list")

        data = {"title": "test_board", "description": "test_board"}

        response = user_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED, response.data

    def test_게스트는_보드를_만들_수_없다(self, set_credentials):
        guest = GuestFactory()

        guest_client = set_credentials(guest)

        url = reverse("boards-list")

        data = {"title": "test_board", "description": "test_board"}

        response = guest_client.post(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
