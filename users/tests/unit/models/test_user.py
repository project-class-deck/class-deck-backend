import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user():
    test_user = User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpassword123",
        nickname="testnickname",
        grade=1,
        classroom=1,
    )
    return test_user


@pytest.mark.django_db
def test_new_user(user):
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
    assert user.nickname == "testnickname"
    assert user.grade == 1
    assert user.classroom == 1
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_new_superuser():
    User = get_user_model()
    admin_user = User.objects.create_superuser(
        username="superadmin",
        email="superadmin@example.com",
        password="testpassword123",
    )
    assert admin_user.username == "superadmin"
    assert admin_user.email == "superadmin@example.com"
    assert admin_user.is_active
    assert admin_user.is_staff
    assert admin_user.is_superuser
