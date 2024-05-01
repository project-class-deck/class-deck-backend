from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BoardViewSet,
    CardCreateAPIView,
    CommentAPIView,
    CommentCreateAPIView,
    LikeAPIView,
    PostViewSet,
)

router = DefaultRouter()
router.register(r"boards", BoardViewSet, basename="boards")
router.register(r"posts", PostViewSet, basename="posts")


urlpatterns = [
    path("", include(router.urls)),
    path("cards/", CardCreateAPIView.as_view(), name="card-create"),
    path(
        "comments/<str:model_slug>/<int:pk>/",
        CommentCreateAPIView.as_view(),
        name="comment",
    ),
    path("comments/<int:pk>/", CommentAPIView.as_view(), name="comment-detail"),
    path("likes/<str:model_slug>/<int:pk>/", LikeAPIView.as_view(), name="like"),
]
