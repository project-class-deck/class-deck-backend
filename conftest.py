import pytest
from django.core.management import call_command
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def set_credentials(client):
    def user_to_client(user):
        token = AccessToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
        client.user = user
        return client

    return user_to_client


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture(scope="session", autouse=True)
def seed_db(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("seed_cards")
        call_command("seed_groups")
