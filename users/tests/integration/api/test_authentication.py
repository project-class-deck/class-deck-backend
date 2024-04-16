import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.fixture
def user():
    test_user = User.objects.create_user(
        username="john", email="john@example.com", password="s3cr3t"
    )
    return test_user


@pytest.mark.django_db
def test_가입할_할_수_있다(client):
    response = client.post(
        reverse("user-register"),
        {
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpassword1!",
            "nickname": "testnickname",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["username"] == "testuser"
    assert response.data["nickname"] == "testnickname"

    assert User.objects.filter(username="testuser").exists()
    test_user = User.objects.get(username="testuser")

    assert test_user.nickname == "testnickname"
    assert test_user.grade == 1
    assert test_user.classroom == 1
    assert test_user.email == "test@test.com"
    assert test_user.is_active is True
    assert test_user.is_staff is False


@pytest.mark.django_db
def test_login_with_valid_credentials(client, user):
    url = reverse("rest_login")
    data = {"username": "john", "password": "s3cr3t"}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data
    login_user = response.data["user"]
    assert login_user["username"] == "john"
    assert login_user["email"] == "john@example.com"


@pytest.mark.django_db
def test_login_with_invalid_credentials(client):
    url = reverse("rest_login")
    data = {"username": "john", "password": "wrongpassword"}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "non_field_errors" in response.data
