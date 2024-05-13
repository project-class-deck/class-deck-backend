import pytest
from django.urls import reverse
from rest_framework import status

from content.tests.factories import BoardFactory, PostFactory
from users.tests.factories import GuestFactory, UserFactory


@pytest.mark.django_db
class TestPostUpdateAPI:
    def setup_method(self):
        BoardFactory.create()

    def test_권한이_없는_사용자는_게시글을_수정할_수_없다(self, set_credentials):
        author = UserFactory()

        post = PostFactory.create(author=author)

        url = reverse("posts-detail", kwargs={"pk": post.pk})

        user = UserFactory()

        user_client = set_credentials(user)

        data = {"title": "test_post", "content": "test_post"}

        response = user_client.put(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN, response.data

    def test_권한_있는_사용자는_게시글을_수정할_수_있다(self, set_credentials):
        author = UserFactory()

        post = PostFactory.create(author=author)

        url = reverse("posts-detail", kwargs={"pk": post.pk})

        user_client = set_credentials(author)

        data = {"title": "test_post", "content": "test_post"}

        response = user_client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK, response.data

    def test_권한_있는_게스트는_게시글을_수정할_수_있다(self, set_credentials):
        author = GuestFactory()

        post = PostFactory.create(author=author)

        url = reverse("posts-detail", kwargs={"pk": post.pk})

        user_client = set_credentials(author)

        data = {"title": "test_post", "content": "test_post"}

        response = user_client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK, response.data
