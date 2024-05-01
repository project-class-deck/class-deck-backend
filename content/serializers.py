from django.db.models import Q
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Board, Card, Comment, Like, Post


class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["title", "description", "author"]
        read_only_fields = ("created_at", "updated_at")


class BoardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["title", "description", "author"]
        read_only_fields = ("author", "created_at", "updated_at")


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        # TODO id도 포함시키기
        exclude = ("id", "board", "image", "created_at", "updated_at")


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


# 댓글 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "content_type",
            "object_id",
            "author",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("created_at", "updated_at")


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["content_type", "object_id", "user", "created_at"]
        read_only_fields = ("created_at",)
