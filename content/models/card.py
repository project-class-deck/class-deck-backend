from django.contrib.auth import get_user_model
from django.db import models

from .board import Board

User = get_user_model()


class Card(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="cards")

    image = models.ImageField(upload_to="images/cards/")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
