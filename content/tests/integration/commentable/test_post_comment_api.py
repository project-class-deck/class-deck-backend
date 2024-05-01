import pytest
from django.urls import reverse
from rest_framework import status

from content.models import Card
from content.tests.factories import PostFactory
from users.tests.factories import GuestFactory, UserFactory


@pytest.mark.django_db
class TestPostCommentAPI:
    def setup_method(self):
        self.user = UserFactory()
        self.guest = GuestFactory()

        card = Card.objects.get(pk=1)
        self.post = PostFactory(card=card)

    def test_사용자는_게시물에_댓글을_달_수_있다(self, set_credentials):
        user_client = set_credentials(self.user)

        data = {"content": "테스트 댓글입니다"}

        url = reverse("comment", kwargs={"model_slug": "post", "pk": self.post.pk})

        response = user_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED, response.data

    def test_사용자는_게시물에_댓글을_삭제할_수_있다(self, set_credentials):
        user_client = set_credentials(self.user)

        comment = self.post.comment(self.user, "안녕하세요")

        url = reverse("comment-detail", kwargs={"pk": comment.id})

        response = user_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.data

    def test_사용자는_게시물에_남의_댓글을_삭제할_수_없다(self, set_credentials):
        user_client = set_credentials(self.user)

        new_user = UserFactory()

        comment = self.post.comment(new_user, "안녕하세요")

        url = reverse("comment-detail", kwargs={"pk": comment.id})

        response = user_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN, response.data

    def test_게스트는_게시물에_댓글을_달_수_있다(self, set_credentials):
        guest_client = set_credentials(self.guest)

        data = {"content": "테스트 댓글입니다"}

        url = reverse("comment", kwargs={"model_slug": "post", "pk": self.post.pk})

        response = guest_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED, response.data

    def test_게스트는_게시물에_댓글을_삭제할_수_있다(self, set_credentials):
        guest_client = set_credentials(self.guest)

        comment = self.post.comment(self.guest, "안녕하세요")

        url = reverse("comment-detail", kwargs={"pk": comment.id})

        response = guest_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.data

    def test_게스트는_게시물에_남의_댓글을_삭제할_수_없다(self, set_credentials):
        guest_client = set_credentials(self.guest)

        new_user = UserFactory()

        comment = self.post.comment(new_user, "안녕하세요")

        url = reverse("comment-detail", kwargs={"pk": comment.id})

        response = guest_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN, response.data
