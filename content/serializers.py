from django.db.models import Q
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Board, Card, Comment, Like, Post


class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "title", "description", "author"]
        read_only_fields = ("created_at", "updated_at")

        extra_kwargs = {
            "author": {"write_only": True},
        }

    def to_representation(self, instance):
        res = super().to_representation(instance)

        res.update({"author": instance.author.nickname})

        return res


class BoardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["title", "description", "author"]
        read_only_fields = ("author", "created_at", "updated_at")


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        exclude = ("board", "image", "created_at", "updated_at")


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.nickname")
    date = serializers.ReadOnlyField(source="created_at")
    thumbnail = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "card",
            "author",
            "date",
            "thumbnail",
            "content",
            "likes",
            "comments",
            "is_public",
            "updated_at",
        ]

    def get_thumbnail(self, obj) -> str:
        return obj.card.image_front

    def get_likes(self, obj) -> int:
        return obj.like_count()

    def get_comments(self, obj) -> int:
        return obj.comments.count()


class BoardDetailSerializer(BoardCreateSerializer):
    cards = SerializerMethodField()
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "description",
            "author",
            "cards",
            "posts",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("author", "created_at", "updated_at")

    @extend_schema_field(CardSerializer(many=True))
    def get_cards(self, obj):
        cards = Card.objects.filter(Q(board=obj) | Q(board__isnull=True))

        return CardSerializer(cards, many=True).data


class CardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source="author.id")

    class Meta:
        model = Comment
        fields = [
            "id",
            "content_type",
            "object_id",
            "user_id",
            "author",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")
        extra_kwargs = {
            "content_type": {"write_only": True},
            "object_id": {"write_only": True},
        }

    def to_representation(self, instance):
        res = super().to_representation(instance)

        res.update({"author": instance.author.nickname})

        return res


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["content_type", "object_id", "user", "created_at"]
        read_only_fields = ("created_at",)
