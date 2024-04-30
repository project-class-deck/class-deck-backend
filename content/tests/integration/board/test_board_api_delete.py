import pytest
from django.urls import reverse
from rest_framework import status

from content.tests.factories import BoardFactory
from users.tests.factories import GuestFactory, UserFactory


@pytest.mark.django_db
class TestBoardDeleteAPI:
    def setup_method(self):
        self.user = UserFactory()
        self.board = BoardFactory(author=self.user)
        self.url = reverse("boards-detail", kwargs={"pk": self.board.id})

    def test_비로그인_사용자는_보드를_삭제할_수_없다(self, client):
        response = client.delete(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_게스트는_보드를_삭제할_수_없다(self, set_credentials):
        guest = GuestFactory()

        guest_client = set_credentials(guest)

        response = guest_client.delete(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_로그인_사용자는_본인의_보드를_삭제할_수_있다(self, set_credentials):
        user_client = set_credentials(self.user)

        response = user_client.delete(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_로그인_사용자는_다른_사람의_보드를_삭제할_수_없다(self, set_credentials):
        user_client = set_credentials(self.user)

        new_board = BoardFactory()

        url = reverse("boards-detail", kwargs={"pk": new_board.id})

        response = user_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
