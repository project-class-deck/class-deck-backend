import pytest

from users.models import School


@pytest.fixture
def test_school():
    school = School.objects.create(name="Test School", address="123 Test Street")
    return school


def test_new_school(test_school):
    assert test_school.name == "Test School"
    assert test_school.address == "123 Test Street"
