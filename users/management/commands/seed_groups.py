from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

User = get_user_model()


def create_permission_group_for_user():
    group = Group.objects.create(name="User")

    permissions = Permission.objects.filter(
        codename__in=[
            "add_board",
            "change_board",
            "delete_board",
            "add_post",
            "change_post",
            "delete_post",
            "add_comment",
            "change_comment",
            "delete_comment",
            "add_like",
            "delete_like",
        ]
    )

    group.permissions.set(permissions)


def create_permission_group_for_guest():
    group = Group.objects.create(name="Guest")

    permissions = Permission.objects.filter(
        codename__in=[
            "add_post",
            "change_post",
            "delete_post",
            "add_comment",
            "change_comment",
            "delete_comment",
            "add_like",
            "delete_like",
        ]
    )

    group.permissions.set(permissions)


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_permission_group_for_user()
        create_permission_group_for_guest()
