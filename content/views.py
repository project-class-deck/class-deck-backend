from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response

from .models import Board, Card, Comment, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    BoardCreateSerializer,
    BoardDetailSerializer,
    BoardUpdateSerializer,
    CardCreateSerializer,
    CommentSerializer,
    PostSerializer,
)


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardCreateSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthorOrReadOnly,
    )

    def get_queryset(self):
        if self.action == "retrieve":
            return Board.objects.prefetch_related("cards")
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BoardDetailSerializer
        elif self.action == "update":
            return BoardUpdateSerializer

        return super().get_serializer_class()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthorOrReadOnly,
    )

    @action(detail=True, methods=["post"], url_path="like")
    def like_post(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        created, like = post.like(request.user)

        if created:
            return Response({"status": "liked"})
        else:
            like.delete()
            return Response({"status": "unliked"})


class CardCreateAPIView(generics.CreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardCreateSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 코멘트 뷰셋
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthorOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
