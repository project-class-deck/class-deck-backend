from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Board, Card, Comment, Like, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    BoardCreateSerializer,
    BoardDetailSerializer,
    BoardUpdateSerializer,
    CardCreateSerializer,
    CommentSerializer,
    LikeSerializer,
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


class CommentCreateAPIView(APIView):
    queryset = Comment.objects.all()
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthorOrReadOnly,
    )

    def post(self, request, *args, **kwargs):
        content_type = get_object_or_404(
            ContentType, model=kwargs["model_slug"].lower()
        )
        data = {
            "author": request.user.id,
            "content_type": content_type.id,
            "object_id": kwargs["pk"],
            "content": request.data["content"],
        }

        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentAPIView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthorOrReadOnly,
    )


class LikeAPIView(GenericAPIView):
    queryset = Like.objects.all()
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthorOrReadOnly,
    )

    def post(self, request, *args, **kwargs):
        content_type = get_object_or_404(
            ContentType, model=kwargs["model_slug"].lower()
        )
        data = {
            "user": request.user.id,
            "content_type": content_type.id,
            "object_id": kwargs["pk"],
        }

        serializer = LikeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        content_type = get_object_or_404(
            ContentType, model=kwargs["model_slug"].lower()
        )
        data = {
            "content_type": content_type.id,
            "object_id": kwargs["pk"],
        }

        instance = Like.objects.filter(**data).get()
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
