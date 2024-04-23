import factory
from factory.django import DjangoModelFactory

from content.models import Board
from users.tests.factories.user_factory import UserFactory


class BoardFactory(DjangoModelFactory):
    class Meta:
        model = Board
        skip_postgeneration_save = True

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("sentence", nb_words=10)
    owner = factory.SubFactory(UserFactory)

    created_at = factory.Faker("date_time_this_month")
    updated_at = factory.Faker("date_time_this_month")
