import pytest
from django.urls import reverse
from rest_framework import status

from content.models import Card
from content.tests.factories import PostFactory
from users.tests.factories import UserFactory


@pytest.mark.django_db
class TestPostLikeAPI:
    def setup_method(self):
        self.user = UserFactory()

        card = Card.objects.get(pk=1)
        self.post = PostFactory(card=card)

        self.url = reverse("like", kwargs={"model_slug": "post", "pk": self.post.pk})

    def test_사용자는_게시물에_좋아요를_누를_수_있다(self, set_credentials):
        user_client = set_credentials(self.user)

        response = user_client.post(self.url)

        assert response.status_code == status.HTTP_201_CREATED, response.data

    def test_사용자는_게시물에_좋아요를_취소할_수_있다(self, set_credentials):
        self.post.like(self.user)

        user_client = set_credentials(self.user)

        response = user_client.delete(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.data

    def test_사용자는_게시물의_남의_좋아요를_취소할_수_없다(self, set_credentials):
        new_user = UserFactory()

        self.post.like(new_user)

        user_client = set_credentials(self.user)

        response = user_client.delete(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN, response.data
