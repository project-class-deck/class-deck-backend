import json

from django.core.management.base import BaseCommand

from content.models import Card


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = "assets/cards.json"
        with open(file_path, "r") as f:
            cards = json.load(f)
            for card in cards:
                Card.objects.update_or_create(**card)
