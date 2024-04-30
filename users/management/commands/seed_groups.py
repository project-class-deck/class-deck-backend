from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

User = get_user_model()


def create_permission_group_for_user():
    group = Group.objects.create(name="User")

    group.permissions.set(
        [
            Permission.objects.get(codename="add_board"),
            Permission.objects.get(codename="change_board"),
            Permission.objects.get(codename="add_post"),
            Permission.objects.get(codename="change_post"),
        ]
    )


def create_permission_group_for_guest():
    group = Group.objects.create(name="Guest")
    group.permissions.set(
        [
            Permission.objects.get(codename="add_post"),
            Permission.objects.get(codename="change_post"),
        ]
    )


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_permission_group_for_user()
        create_permission_group_for_guest()
