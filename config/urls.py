from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [

    # Django Admin
    path("admin/", admin.site.urls),

    # OpenAPI / Swagger
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema"
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui"
    ),

    path(
        "api/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema"
        ),
        name="redoc"
    ),

    # JWT
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),



    path(
        "api/buildings/",
        include("apps.building.urls")
    ),

    path(
        "api/wings/",
        include("apps.wing.urls")
    ),

    path(
        "api/flats/",
        include("apps.flats.urls")
    ),

    path(
        "api/users/",
        include("apps.users.urls")
    ),

    path(
        "api/income/",
        include("apps.income.urls")
    ),

    path(
        "api/expense/",
        include("apps.expense.urls")
    ),

    path(
        "api/complaint/",
        include("apps.complaint.urls")
    ),

    path(
        "api/notice/",
        include("apps.notice.urls")
    ),

    path(
        "api/maintenance/",
        include("apps.maintenance.urls")
    ),
]

# Media Files

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )