from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


def create_superuser():
    username = settings.ADMIN_USERNAME
    password = settings.ADMIN_PASSWORD
    email = settings.ADMIN_EMAIL

    User.objects.create_superuser(username, email, password)


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_superuser()
