import pytest
from django.contrib.auth import get_user_model

from content.models import Board
from users.tests.factories import UserFactory

User = get_user_model()


@pytest.mark.django_db
def test_보드를_생성할_수_있다():
    user = UserFactory()
    board = Board.objects.create(
        author=user,
        title="new board",
        description="it's new board",
    )

    assert board.author == user
    assert board.title == "new board"
    assert board.description == "it's new board"

    assert board.created_at is not None
    assert board.updated_at is not None


@pytest.mark.django_db
def test_사용자는_보드에_좋아요를_추가할_수_있다():
    user = UserFactory()
    board = Board.objects.create(
        author=user,
        title="new board",
        description="it's new board",
    )

    board.like(user)

    assert board.likes.filter(user=user).exists()
    assert board.is_liked(user) is True
    assert board.get_liked_users() == [user]
    assert board.like_count() == 1


@pytest.mark.django_db
def test_사용자는_보드에_좋아요를_취소할_수_있다():
    user = UserFactory()
    board = Board.objects.create(
        author=user,
        title="new board",
        description="it's new board",
    )

    board.like(user)

    assert board.likes.filter(user=user).exists()
    assert board.is_liked(user) is True
    assert board.get_liked_users() == [user]
    assert board.like_count() == 1

    board.unlike(user)

    assert board.like_count() == 0


@pytest.mark.django_db
def test_사용자가_삭제되면_사용자의_보드도_삭제된다():
    user = UserFactory()
    board = Board.objects.create(
        author=user,
        title="new board",
        description="it's new board",
    )

    user.delete()

    assert not Board.objects.filter(id=board.id).exists()
