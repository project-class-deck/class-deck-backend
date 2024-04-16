from django.contrib.auth import get_user_model
from django.db import models

from ..mixins import Commentable, Likeable
from .card import Card

User = get_user_model()


class Post(Commentable, Likeable, models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="posts")

    title = models.CharField(max_length=255)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
