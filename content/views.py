from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Board, Comment, Like, Post
from .serializers import BoardSerializer, CommentSerializer, PostSerializer


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


# 포스트 뷰셋
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # PostViewSet 내부
    @action(detail=True, methods=["post"], url_path="like")
    def like_post(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            return Response({"status": "liked"})
        else:
            like.delete()
            return Response({"status": "unliked"})


# 코멘트 뷰셋
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
