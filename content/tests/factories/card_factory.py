import factory
from factory.django import DjangoModelFactory

from content.models import Card
from content.tests.factories.board_factory import BoardFactory


class CardFactory(DjangoModelFactory):
    class Meta:
        model = Card
        skip_postgeneration_save = True

    board = factory.SubFactory(BoardFactory)
    image = factory.django.ImageField(from_path="content/tests/factories/test.jpg")

    no = factory.Faker("random_int", min=1, max=504)
    description = factory.Faker("sentence", nb_words=4)
    meaning = factory.Faker("sentence", nb_words=10)
    example = factory.Faker("sentence", nb_words=10)
    cardSet = factory.Faker("random_int", min=1, max=504)
    category = factory.Faker("sentence", nb_words=4)

    image_front = factory.Faker("sentence", nb_words=4)
    image_back = factory.Faker("sentence", nb_words=4)

    front_image_size_w = factory.Faker("random_int", min=100, max=1000)
    front_image_size_h = factory.Faker("random_int", min=100, max=1000)
    back_image_size_w = factory.Faker("random_int", min=100, max=1000)
    back_image_size_h = factory.Faker("random_int", min=100, max=1000)
    zoom_ratio = factory.Faker("random_int", min=1, max=100)

    created_at = factory.Faker("date_time_this_month")
    updated_at = factory.Faker("date_time_this_month")
