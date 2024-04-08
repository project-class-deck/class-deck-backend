from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoardViewSet

# 라우터 생성 및 뷰셋 등록
router = DefaultRouter()
router.register(r'boards', BoardViewSet)

urlpatterns = [
    path('', include(router.urls)),  # 라우터 URL 포함
]
