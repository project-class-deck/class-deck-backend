import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def set_credentials():
    def user_to_client(user):
        token = AccessToken.for_user(user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
        client.user = user
        return client

    return user_to_client
