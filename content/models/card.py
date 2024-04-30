from django.contrib.auth import get_user_model
from django.db import models

from .board import Board

User = get_user_model()


class Card(models.Model):
    board = models.ForeignKey(
        Board, null=True, on_delete=models.CASCADE, related_name="cards"
    )
    image = models.ImageField(upload_to="images/cards/", blank=True, null=True)

    no = models.PositiveIntegerField()
    description = models.CharField(blank=True, max_length=50)
    meaning = models.CharField(blank=True, max_length=255)
    example = models.CharField(blank=True, max_length=255)
    cardSet = models.PositiveSmallIntegerField()
    category = models.CharField(blank=True, max_length=50)
    image_front = models.CharField(blank=True, max_length=50)
    image_back = models.CharField(blank=True, max_length=50)

    front_image_size_w = models.PositiveSmallIntegerField()
    front_image_size_h = models.PositiveSmallIntegerField()
    back_image_size_w = models.PositiveSmallIntegerField()
    back_image_size_h = models.PositiveSmallIntegerField()
    zoom_ratio = models.PositiveIntegerField(default=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.board} no.{self.no} {self.image_front}"
