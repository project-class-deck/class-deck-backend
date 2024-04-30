import pytest
from django.contrib.auth import get_user_model

from content.models import Post
from content.tests.factories import BoardFactory
from content.tests.factories.card_factory import CardFactory
from users.tests.factories.user_factory import UserFactory

User = get_user_model()


@pytest.mark.django_db
def test_게시물을_생성할_수_있다():
    user = UserFactory()
    board = BoardFactory()
    card = CardFactory()

    post = Post.objects.create(
        author=user,
        board=board,
        card=card,
        title="new post",
        content="it's new post",
    )

    assert post.author == user
    assert post.card == card
    assert post.title == "new post"
    assert post.content == "it's new post"
    assert post.is_public is True
