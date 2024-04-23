import uuid

import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        skip_postgeneration_save = True

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password123")
    nickname = factory.Faker("name")


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        skip_postgeneration_save = True

    username = uuid.uuid4().hex[:30]
    email = ""
    password = factory.PostGenerationMethodCall("set_password", "password123")
    nickname = factory.Faker("name")
