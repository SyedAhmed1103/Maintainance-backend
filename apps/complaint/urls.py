# apps/complaint/urls.py

from django.urls import path

from .views import (
    ComplaintListAPIView,
    ComplaintCreateAPIView,
    ComplaintDetailAPIView,
    ComplaintUpdateAPIView,
    ComplaintDeleteAPIView,
)

urlpatterns = [

    path(
        "",
        ComplaintListAPIView.as_view(),
        name="complaint-list",
    ),

    path(
        "create/",
        ComplaintCreateAPIView.as_view(),
        name="complaint-create",
    ),

    path(
        "<int:pk>/",
        ComplaintDetailAPIView.as_view(),
        name="complaint-detail",
    ),

    path(
        "<int:pk>/update/",
        ComplaintUpdateAPIView.as_view(),
        name="complaint-update",
    ),

    path(
        "<int:pk>/delete/",
        ComplaintDeleteAPIView.as_view(),
        name="complaint-delete",
    ),
]