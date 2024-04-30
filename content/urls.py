from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BoardViewSet, CardCreateAPIView, CommentViewSet, PostViewSet

router = DefaultRouter()
router.register(r"boards", BoardViewSet, basename="boards")
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"comments", CommentViewSet, basename="comments")


urlpatterns = [
    path("", include(router.urls)),
    path("cards/", CardCreateAPIView.as_view(), name="card-create"),
]
