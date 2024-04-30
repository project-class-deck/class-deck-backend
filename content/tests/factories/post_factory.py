import factory
from factory.django import DjangoModelFactory

from content.models import Post
from content.tests.factories import BoardFactory
from content.tests.factories.card_factory import CardFactory


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
        skip_postgeneration_save = True

    card = factory.SubFactory(CardFactory)
    board = factory.SubFactory(BoardFactory)
    author = factory.SubFactory("users.tests.factories.user_factory.UserFactory")

    title = factory.Faker("sentence", nb_words=4)
    content = factory.Faker("sentence", nb_words=10)
    is_public = factory.Faker("boolean", chance_of_getting_true=75)

    created_at = factory.Faker("date_time_this_month")
    updated_at = factory.Faker("date_time_this_month")
