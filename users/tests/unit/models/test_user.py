import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()


@pytest.mark.django_db
def test_user를_생성할_수_있다():
    user = User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpassword123",
        nickname="testnickname",
    )

    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
    assert user.nickname == "testnickname"
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_username을_중복해서_생성할_수_없다():
    User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpassword123",
        nickname="testnickname",
    )

    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username="testuser",
            email="testuser1@example.com",
            password="testpassword123",
            nickname="testnickname1",
        )


@pytest.mark.django_db
def test_닉네임을_중복해서_생성할_수_있다():
    User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpassword123",
        nickname="testnickname",
    )

    try:
        User.objects.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password="testpassword123",
            nickname="testnickname",
        )
    except IntegrityError:
        pytest.fail("IntegrityError 예외가 발생했습니다.")


@pytest.mark.django_db
def test_이메일을_중복해서_생성할_수_있다():
    User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpassword123",
        nickname="testnickname",
    )

    try:
        User.objects.create_user(
            username="testuser1",
            email="testuser@example.com",
            password="testpassword123",
            nickname="testnickname1",
        )
    except IntegrityError:
        pytest.fail("IntegrityError 예외가 발생했습니다.")


@pytest.mark.django_db
def test_superuser를_생성할_수_있다():
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
