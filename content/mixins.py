from django.contrib.contenttypes.models import ContentType
from django.db import models

from .models.comment import Comment
from .models.like import Like


class Likeable(models.Model):
    class Meta:
        abstract = True

    def get_likes(self):
        """
        Retrieves all likes associated with this instance.
        """
        return Like.objects.filter(
            content_type=ContentType.objects.get_for_model(self), object_id=self.id
        )


class Commentable(models.Model):
    class Meta:
        abstract = True

    def get_comments(self):
        """
        Retrieves all likes associated with this instance.
        """
        return Comment.objects.filter(
            content_type=ContentType.objects.get_for_model(self), object_id=self.id
        )
