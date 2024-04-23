from django.contrib.auth import get_user_model
from django.db import models

from ..mixins import Commentable, CommentableManager, Likeable, LikeableManager
from .card import Card

User = get_user_model()


class Post(Commentable, Likeable, models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="posts")

    title = models.CharField(max_length=255)
    content = models.TextField()
    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = "PostManager"

    def __str__(self):
        return self.title


class PostManager(CommentableManager, LikeableManager, models.Manager):
    def public(self):
        return self.filter(is_public=True)
