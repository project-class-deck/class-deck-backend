import datetime

import pytest
from django.urls import reverse
from rest_framework import status

from content.models import Board, Card
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
        assert response.data["count"] == 10

    def test_로그인_사용자는_보드_목록을_볼_수_있다(self, set_credentials):
        user = UserFactory()

        user_client = set_credentials(user)

        BoardFactory.create_batch(10)

        url = reverse("boards-list")

        response = user_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["is_displayed"] is True, response.data
        assert response.data["results"][0]["slug"] != "", response.data
        assert response.data["count"] == 10

    def test_학생_사용자는_보드_목록을_볼_수_있다(self, set_credentials):
        user = GuestFactory()

        guest_client = set_credentials(user)

        BoardFactory.create_batch(10)

        url = reverse("boards-list")

        response = guest_client.get(url)

        assert Board.objects.count() == 10

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 10


@pytest.mark.django_db
def test_사용자는_보드의_정보를_확인할_수_있다(set_credentials, cards_json_list):
    user = UserFactory()

    user_client = set_credentials(user)

    board = BoardFactory()

    url = reverse("boards-detail", kwargs={"slug": board.slug})

    response = user_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == board.id
    assert response.data["title"] == board.title
    assert response.data["description"] == board.description
    assert response.data["author"] == board.author.nickname
    assert response.data["user_id"] == board.author.id
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


def exclude_id_key(dictionary):
    return [{k: v for k, v in card.items() if k != "id"} for card in dictionary]


@pytest.mark.django_db
class TestBoardDetailCardAPI:
    def setup_method(self):
        self.board = BoardFactory()
        self.url = reverse("boards-detail", kwargs={"slug": self.board.slug})

    def test_비로그인_사용자는_보드의_카드를_확인할_수_있다(
        self, client, cards_json_list
    ):
        response = client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert exclude_id_key(response.data["cards"]) == cards_json_list

    def test_로그인_사용자는_보드의_카드를_확인할_수_있다(
        self, set_credentials, cards_json_list
    ):
        user = UserFactory()

        user_client = set_credentials(user)

        response = user_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["is_displayed"] == self.board.is_displayed
        assert exclude_id_key(response.data["cards"]) == cards_json_list

    def test_게스트는_보드의_카드를_확인할_수_있다(
        self, set_credentials, cards_json_list
    ):
        guest = GuestFactory()

        guest_client = set_credentials(guest)

        response = guest_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert exclude_id_key(response.data["cards"]) == cards_json_list


@pytest.mark.django_db
class TestBoardDetailPostAPI:
    def setup_method(self):
        self.board = BoardFactory()
        self.card = Card.objects.get(pk=1)
        self.url = reverse("boards-detail", kwargs={"slug": self.board.slug})

    def test_비로그인_사용자는_보드의_게시물을_확인할_수_있다(
        self, client, cards_json_list
    ):
        card = Card.objects.get(pk=1)

        post = PostFactory(
            board=self.board, card=card, title="제목입니다", content="글을 작성합니다"
        )

        response = client.get(self.url)

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

        response = user_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["posts"][0]["id"] == post.id
        assert response.data["posts"][0]["title"] == post.title
        assert response.data["posts"][0]["author"] == post.author.nickname
        assert (
            response.data["posts"][0]["created_at"]
            == post.created_at.astimezone(
                datetime.timezone(datetime.timedelta(hours=9))
            ).isoformat()
        )
        assert response.data["posts"][0]["thumbnail"] == post.card.image_front
        assert response.data["posts"][0]["content"] == post.content
        assert response.data["posts"][0]["likes"] == post.like_count()
        assert response.data["posts"][0]["comments"] == post.comments.count()
        assert response.data["posts"][0]["is_liked"] is False

        my_post = PostFactory(
            board=self.board,
            card=self.card,
            title="내 게시글 제목입니다",
            content="글을 작성합니다",
            author=user,
        )

        response = user_client.get(self.url)

        assert response.data["posts"][1]["id"] == my_post.id
        assert response.data["posts"][1]["is_author"] is True

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

        response = guest_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["posts"] == PostSerializer([post], many=True).data
