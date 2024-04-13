import pytest
from django.contrib.auth import get_user_model

from users.models import School

User = get_user_model()


@pytest.mark.django_db
def test_가입할_할_수_있다(client):
    school = School.objects.create(name="Test School", address="123 Test Street")
    response = client.post(
        "/users/register/",
        {
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpassword1!",
            "nickname": "testnickname",
            "school": school.id,
            "grade": 1,
            "classroom": 1,
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["username"] == "testuser"
    assert response.data["nickname"] == "testnickname"
    assert response.data["grade"] == 1
    assert response.data["classroom"] == 1

    assert User.objects.filter(username="testuser").exists()
    user = User.objects.get(username="testuser")

    assert user.nickname == "testnickname"
    assert user.grade == 1
    assert user.classroom == 1
    assert user.email == "test@test.com"
    assert user.is_active is True
    assert user.is_staff is False
