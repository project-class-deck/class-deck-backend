from django.contrib.auth import get_user_model
from django.db import models

from ..mixins import Likeable

User = get_user_model()


class Board(Likeable, models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="boards")
    is_displayed = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
