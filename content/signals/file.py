import os

from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


@receiver(pre_save)
def auto_delete_file_on_save(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False

    for field in instance._meta.fields:
        if isinstance(field, (models.FileField, models.ImageField)):
            origin_file = getattr(old_obj, field.name)
            new_file = getattr(instance, field.name)
            if origin_file != new_file and os.path.isfile(origin_file.path):
                os.remove(origin_file.path)


@receiver(post_delete)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if isinstance(field, (models.FileField, models.ImageField)):
            origin_file = getattr(instance, field.name)
            if origin_file and os.path.isfile(origin_file.path):
                os.remove(origin_file.path)
