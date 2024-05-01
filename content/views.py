from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, viewsets
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


@extend_schema(tags=["Boards"])
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


@extend_schema(tags=["Posts"])
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthorOrReadOnly,
    )


@extend_schema(tags=["Cards"])
class CardCreateAPIView(generics.CreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardCreateSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


@extend_schema(tags=["Comments"])
class CommentCreateAPIView(APIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthorOrReadOnly,
    )

    def get(self, request, *args, **kwargs):
        content_type = get_object_or_404(
            ContentType, model=kwargs["model_slug"].lower()
        )

        comments = Comment.objects.filter(
            content_type=content_type, object_id=kwargs["pk"]
        )

        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

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


@extend_schema(tags=["Comments"])
class CommentAPIView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthorOrReadOnly,
    )


@extend_schema(tags=["Likes"])
class LikeAPIView(GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
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
