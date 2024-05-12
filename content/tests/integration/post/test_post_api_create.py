import pytest
from django.urls import reverse
from rest_framework import status

from content.tests.factories import BoardFactory
from users.tests.factories import GuestFactory, UserFactory


@pytest.mark.django_db
class TestPostCreateAPI:
    def setup_method(self):
        BoardFactory.create()

    def test_비로그인_사용자는_게시글을_만들_수_없다(self, client):
        url = reverse("posts-list")

        data = {"title": "test_post", "content": "test_post", "board": 1, "card": 1}

        response = client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.data

    def test_로그인_사용자는_게시글을_만들_수_있다(self, set_credentials):
        user = UserFactory()

        user_client = set_credentials(user)

        url = reverse("posts-list")

        data = {"title": "test_post", "content": "test_post", "board": 1, "card": 1}

        response = user_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED, response.data

    def test_게스트는_게시글을_만들_수_있다(self, set_credentials):
        guest = GuestFactory()

        guest_client = set_credentials(guest)

        url = reverse("posts-list")

        data = {"title": "test_post", "content": "test_post", "board": 1, "card": 1}

        response = guest_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED, response.data

    def test_카드_없이도_게시글을_말들_수_있다(self, set_credentials):
        user = UserFactory()

        user_client = set_credentials(user)

        url = reverse("posts-list")

        data = {"title": "test_post", "content": "test_post", "board": 1}

        response = user_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED, response.data
