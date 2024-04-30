from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Guest

User = get_user_model()


@receiver(post_save, sender=User)
def add_user_to_group_on_save(sender, instance, **kwargs):
    group = Group.objects.get(name="User")
    instance.groups.add(group)


@receiver(post_save, sender=Guest)
def add_guest_to_group_on_save(sender, instance, **kwargs):
    group = Group.objects.get(name="Guest")
    instance.groups.add(group)
