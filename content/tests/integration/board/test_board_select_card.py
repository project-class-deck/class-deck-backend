import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status

from content.tests.factories import BoardFactory
from users.tests.factories import UserFactory


@pytest.mark.django_db
class TestBoardSelectCardAPI:
    def setup_method(self):
        self.user = UserFactory()
        self.board = BoardFactory(author=self.user)
        self.url = reverse("boards-detail", kwargs={"slug": self.board.slug})

    def test_사용자는_카드를_선택할_수_있다(self, set_credentials):
        url = reverse("boards-select", kwargs={"slug": self.board.slug})

        user_client = set_credentials(self.user)

        response = user_client.post(f"{url}?card=2")

        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data.get("count") == 1
        assert response.data.get("users") == [self.user.nickname]

        new_user = UserFactory()

        new_user_client = set_credentials(new_user)

        response = new_user_client.post(f"{url}?card=2")

        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data.get("count") == 2
        assert set(response.data.get("users")) == {
            self.user.nickname,
            new_user.nickname,
        }

    def test_사용자는_카드_선택을_해제_수_있다(self, set_credentials):
        select_url = reverse("boards-select", kwargs={"slug": self.board.slug})
        deselect_url = reverse("boards-deselect", kwargs={"slug": self.board.slug})

        user_client = set_credentials(self.user)

        response = user_client.post(f"{select_url}?card=2")

        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data.get("count") == 1
        assert response.data.get("users") == [self.user.nickname]

        response = user_client.delete(f"{deselect_url}?card=2")

        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data.get("count") == 0
        assert response.data.get("users") == []

    def test_사용자는_카드_선택한_목록을_확인할_수_있다(self, set_credentials):
        selected_url = reverse("boards-selected", kwargs={"slug": self.board.slug})

        user_client = set_credentials(self.user)

        cache.set(f"board.{self.board.slug}.card.2", [self.user.nickname])

        response = user_client.get(f"{selected_url}?card=2")

        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data.get("count") == 1
        assert response.data.get("users") == [self.user.nickname]
