from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .models.comment import Comment
from .models.like import Like


class Likeable(models.Model):
    likes = GenericRelation(Like)

    class Meta:
        abstract = True

    def like_count(self):
        """
        Retrieves the number of likes associated with this instance.
        """
        return self.likes.count()

    def is_liked(self, user):
        """
        Checks if a like is associated with this instance.
        """
        return self.likes.filter(user=user).exists()

    def get_liked_users(self):
        return [like.user for like in self.likes.only("user").all()]

    def like(self, user):
        """
        Adds a like to this instance.
        """
        return Like.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
            user=user,
        )

    def unlike(self, user):
        """
        Removes a like from this instance.
        """
        Like.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
            user=user,
        ).delete()


class LikeableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("likes")

    def liked(self, user):
        """
        Retrieves all instances liked by a user.
        """
        return self.filter(likes__user=user)


class Commentable(models.Model):
    comments = GenericRelation(Comment)

    class Meta:
        abstract = True

    def get_comments(self):
        """
        Retrieves all likes associated with this instance.
        """
        return self.comments.filter(
            content_type=ContentType.objects.get_for_model(self), object_id=self.id
        )


class CommentableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("comments")

    def commented(self, user):
        """
        Retrieves all instances commented by a user.
        """
        return self.filter(comments__user=user)
