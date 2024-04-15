from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BoardMembershipRequestViewSet,
    BoardViewSet,
    CategoryViewSet,
    CommentViewSet,
    PostViewSet,
)

# 라우터 생성 및 뷰셋 등록
router = DefaultRouter()
router.register(r"boards", BoardViewSet)
router.register(
    r"membership_requests/<int:id>",
    BoardMembershipRequestViewSet,
    basename="membership-request",
)
router.register(r"categories", CategoryViewSet)
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)


urlpatterns = [
    path("", include(router.urls)),  # 라우터 URL 포함
]
