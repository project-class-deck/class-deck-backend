import pytest
from django.urls import reverse
from rest_framework import status

from content.tests.factories import BoardFactory
from users.tests.factories import GuestFactory, UserFactory


@pytest.mark.django_db
class TestBoardCreateAPI:
    def setup_method(self):
        self.user = UserFactory()
        self.board = BoardFactory(author=self.user)
        self.url = reverse("boards-detail", kwargs={"slug": self.board.slug})

    def test_비로그인_사용자는_보드를_수정할_수_없다(self, client):
        data = {"title": "test_board", "description": "test_board"}

        response = client.patch(self.url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_게스트는_보드를_수정할_수_없다(self, set_credentials):
        guest = GuestFactory()

        guest_client = set_credentials(guest)

        data = {"title": "test_board", "description": "test_board"}

        response = guest_client.patch(self.url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_로그인_사용자는_보드를_수정할_수_있다(self, set_credentials):
        user_client = set_credentials(self.user)

        data = {"title": "test_board", "description": "test_board"}

        response = user_client.patch(self.url, data)

        assert response.status_code == status.HTTP_200_OK, response.data
