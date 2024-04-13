from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Board, BoardMembershipRequest, Category, Comment, Like, Post
from .serializers import (
    BoardMembershipRequestSerializer,
    BoardSerializer,
    CategorySerializer,
    CommentSerializer,
    PostSerializer,
)


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


# 보드에 가입 신청, 기다리기
class BoardMembershipRequestViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = BoardMembershipRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], url_path="approve")
    def approve_membership(self, request, pk=None):
        membership_request = BoardMembershipRequest.objects.get(pk=pk)
        board = membership_request.board

        if request.user != board.owner:
            return Response(
                {"error": "You are not the owner of this board."},
                status=status.HTTP_403_FORBIDDEN,
            )

        membership_request.is_approved = True
        membership_request.save()
        board.members.add(membership_request.user)
        return Response({"status": "membership approved"})


# 카테고리 뷰셋
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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
