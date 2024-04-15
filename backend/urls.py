from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

API_VERSION = "v1"

urlpatterns = [
    path("super-card/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path(f"api/{API_VERSION}/auth/", include("dj_rest_auth.urls")),
    path(f"api/{API_VERSION}/users/", include("users.urls")),
    path(f"api/{API_VERSION}/content/", include("content.urls")),
]
