from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BoardViewSet, CommentViewSet, PostViewSet

# 라우터 생성 및 뷰셋 등록
router = DefaultRouter()
router.register(r"boards", BoardViewSet)
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)


urlpatterns = [
    path("", include(router.urls)),  # 라우터 URL 포함
]
