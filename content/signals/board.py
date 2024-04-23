import json

from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Board, Card


@receiver(post_save, sender=Board)
def create_default_cards(sender, instance, created, **kwargs):
    if created:
        file_path = "assets/cards.json"
        with open(file_path, "r") as f:
            cards = json.load(f)
            for card in cards:
                Card.objects.create(
                    **card,
                    board=instance,
                )
