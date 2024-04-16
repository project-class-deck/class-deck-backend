from django.contrib.auth import get_user_model
from django.db import models

from ..mixins import Likeable

User = get_user_model()


class Board(Likeable, models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="boards")
    title = models.CharField(max_length=255)
    introduction = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnails/boards/")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
