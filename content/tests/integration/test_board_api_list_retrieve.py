import datetime

import pytest
from django.urls import reverse
from rest_framework import status

from content.models import Card
from content.serializers import PostSerializer
from content.tests.factories import BoardFactory, PostFactory
from users.tests.factories import GuestFactory, UserFactory


@pytest.mark.django_db
class TestBoardListAPI:
    def test_비로그인_사용자는_보드_목록을_볼_수_있다(self, client):
        BoardFactory.create_batch(10)
        url = reverse("boards-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 10

    def test_로그인_사용자는_보드_목록을_볼_수_있다(self, set_credentials):
        user = UserFactory()

        user_client = set_credentials(user)

        BoardFactory.create_batch(10)

        url = reverse("boards-list")

        response = user_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 10

    def test_학생_사용자는_보드_목록을_볼_수_있다(self, set_credentials):
        user = GuestFactory()

        guest_client = set_credentials(user)

        BoardFactory.create_batch(10)

        url = reverse("boards-list")

        response = guest_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 10


@pytest.mark.django_db
def test_사용자는_보드의_정보를_확인할_수_있다(set_credentials, cards_json_list):
    user = UserFactory()

    user_client = set_credentials(user)

    board = BoardFactory()

    url = reverse("boards-detail", kwargs={"pk": board.id})

    response = user_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == board.id
    assert response.data["title"] == board.title
    assert response.data["description"] == board.description
    assert response.data["author"] == board.author.id
    assert (
        response.data["created_at"]
        == board.created_at.astimezone(
            datetime.timezone(datetime.timedelta(hours=9))
        ).isoformat()
    )
    assert (
        response.data["updated_at"]
        == board.updated_at.astimezone(
            datetime.timezone(datetime.timedelta(hours=9))
        ).isoformat()
    )


@pytest.mark.django_db
class TestBoardDetailCardAPI:
    def setup_method(self):
        self.board = BoardFactory()

    def test_비로그인_사용자는_보드의_카드를_확인할_수_있다(
        self, client, cards_json_list
    ):
        url = reverse("boards-detail", kwargs={"pk": self.board.id})

        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["cards"] == cards_json_list

    def test_로그인_사용자는_보드의_카드를_확인할_수_있다(
        self, set_credentials, cards_json_list
    ):
        user = UserFactory()

        user_client = set_credentials(user)

        url = reverse("boards-detail", kwargs={"pk": self.board.id})

        response = user_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["cards"] == cards_json_list

    def test_게스트는_보드의_카드를_확인할_수_있다(
        self, set_credentials, cards_json_list
    ):
        guest = GuestFactory()

        guest_client = set_credentials(guest)

        url = reverse("boards-detail", kwargs={"pk": self.board.id})

        response = guest_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["cards"] == cards_json_list


@pytest.mark.django_db
class TestBoardDetailPostAPI:
    def setup_method(self):
        self.board = BoardFactory()
        self.card = Card.objects.get(pk=1)

    def test_비로그인_사용자는_보드의_게시물을_확인할_수_있다(
        self, client, cards_json_list
    ):
        card = Card.objects.get(pk=1)

        post = PostFactory(
            board=self.board, card=card, title="제목입니다", content="글을 작성합니다"
        )

        url = reverse("boards-detail", kwargs={"pk": self.board.id})

        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["posts"] == PostSerializer([post], many=True).data

    def test_로그인_사용자는_보드의_게시물을_확인할_수_있다(
        self, set_credentials, cards_json_list
    ):
        user = UserFactory()

        user_client = set_credentials(user)

        post = PostFactory(
            board=self.board,
            card=self.card,
            title="제목입니다",
            content="글을 작성합니다",
        )

        url = reverse("boards-detail", kwargs={"pk": self.board.id})

        response = user_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["posts"] == PostSerializer([post], many=True).data

    def test_게스트는_보드의_게시물을_확인할_수_있다(
        self, set_credentials, cards_json_list
    ):
        guest = GuestFactory()
        guest_client = set_credentials(guest)

        post = PostFactory(
            board=self.board,
            card=self.card,
            title="제목입니다",
            content="글을 작성합니다",
        )

        url = reverse("boards-detail", kwargs={"pk": self.board.id})

        response = guest_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["posts"] == PostSerializer([post], many=True).data
