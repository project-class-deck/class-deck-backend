from django.db.models import Q
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Board, Card, Comment, Post


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["title", "description", "author"]
        read_only_fields = ("created_at", "updated_at")


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        exclude = ("id", "board", "image", "created_at", "updated_at")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class BoardDetailSerializer(BoardSerializer):
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
        read_only_fields = ("created_at", "updated_at")

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
        fields = "__all__"
