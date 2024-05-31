import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from users.tests.factories.user_factory import UserFactory

User = get_user_model()


@pytest.mark.django_db
class TestUserUpdate:
    def test_사용자_정보를_수정_할_수_있다(self, set_credentials):
        user = UserFactory()

        user_client = set_credentials(user)

        url = reverse("rest_user_details")

        response = user_client.put(url, {"nickname": "new_name"})

        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data["nickname"] == "new_name"
