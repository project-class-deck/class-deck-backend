from random import randint

from django.core.management.base import BaseCommand

from content.models import Card
from content.tests.factories import BoardFactory, PostFactory


class Command(BaseCommand):
    def handle(self, *args, **options):
        boards = BoardFactory.create_batch(10)

        for board in boards:
            pk = randint(1, 500)
            card = Card.objects.get(pk=pk)
            PostFactory.create_batch(10, board=board, card=card)
