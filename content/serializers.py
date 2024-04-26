from rest_framework import serializers

from .models import Board, Card, Comment, Post


# 보드 관련 시리얼라이저
class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"  # 모든 필드를 포함


# 포스트 시리얼라이저
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class CardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


# 댓글 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
