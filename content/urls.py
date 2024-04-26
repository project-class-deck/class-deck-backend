from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BoardViewSet, CardCreateAPIView, CommentViewSet, PostViewSet

router = DefaultRouter()
router.register(r"boards", BoardViewSet)
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("cards/", CardCreateAPIView.as_view(), name="card-create"),
]
