from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from ..models.board import Board


@receiver(pre_save, sender=Board)
def set_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title, allow_unicode=True)
        unique_slug = instance.slug
        num = 1
        while Board.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{instance.slug}-{num}"
            num += 1
        instance.slug = unique_slug
