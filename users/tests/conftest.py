from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


def set_credentials(user):
    token = AccessToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
    client.user = user
    return client
